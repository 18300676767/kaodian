from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta
from typing import List
import jwt
import os
from passlib.context import CryptContext
from database import get_db
from models import User, Province, City, ExamPoint, ExamPaper, ExamQuestion
from schemas import (
    UserCreate, User as UserSchema, UserList, Token, UserLogin, UserUpdate, UserApproval, 
    Province as ProvinceSchema, City as CitySchema, 
    ExamPointCreate, ExamPoint as ExamPointSchema, ExamPointUpdate, ExamPointImport, ExamPointQuery,
    ExamPaperCreate, ExamPaper as ExamPaperSchema, ExamPaperUpdate, ExamPaperQuery,
    ExamQuestionCreate, ExamQuestion as ExamQuestionSchema, ExamQuestionUpdate, ExamQuestionQuery,
    ExamPaperWithQuestions, FileUploadResponse, OllamaExtractionResult
)
from auth import create_access_token, get_current_user, get_password_hash, verify_password
from utils import save_uploaded_file, is_allowed_file
from ollama_service import OllamaService
from config import settings

# 创建数据库表
# models.Base.metadata.create_all(bind=engine) # This line is removed as per the new_code, as the engine is no longer imported.

app = FastAPI(title="高考考点分析系统API", version="1.0.0")

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
        "Cache-Control",
        "Pragma",
        "Expires"
    ],
    expose_headers=["Content-Type", "Content-Length", "Content-Disposition"],
    max_age=86400,
)

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# 健康检查
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow(), "message": "高考考点分析系统API运行正常"}

# 认证相关路由
@app.post("/auth/register", response_model=UserSchema)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 检查邮箱是否已存在
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="邮箱已存在")
    
    # 创建新用户
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        phone=user.phone,
        real_name=user.real_name,
        age=user.age,
        grade=user.grade,
        province_id=user.province_id,
        city_id=user.city_id,
        is_active=True,  # 明确设置默认值
        is_approved=False,  # 明确设置默认值
        is_deleted=False  # 明确设置默认值
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserSchema)
def get_current_user_info(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == current_user.id).first()

# 省份和城市相关路由
@app.get("/provinces", response_model=List[ProvinceSchema])
def get_provinces(db: Session = Depends(get_db)):
    """获取所有省份列表"""
    provinces = db.query(Province).all()
    return provinces

@app.get("/provinces/{province_id}/cities", response_model=List[CitySchema])
def get_cities_by_province(province_id: int, db: Session = Depends(get_db)):
    """根据省份ID获取城市列表"""
    cities = db.query(City).filter(City.province_id == province_id).all()
    return cities

# 用户管理相关路由
@app.get("/users", response_model=List[UserList])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户列表"""
    users = db.query(User).filter(
        (User.is_deleted == False) | (User.is_deleted.is_(None))
    ).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """获取单个用户信息"""
    user = db.query(User).filter(
        User.id == user_id,
        (User.is_deleted == False) | (User.is_deleted.is_(None))
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@app.put("/users/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新用户信息"""
    db_user = db.query(User).filter(
        User.id == user_id,
        (User.is_deleted == False) | (User.is_deleted.is_(None))
    ).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新字段
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = pwd_context.hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/users/{user_id}/approve", response_model=UserSchema)
def approve_user(
    user_id: int,
    approval: UserApproval,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """审核用户"""
    db_user = db.query(User).filter(
        User.id == user_id,
        (User.is_deleted == False) | (User.is_deleted.is_(None))
    ).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    db_user.is_approved = approval.is_approved
    if approval.is_approved:
        db_user.approved_at = datetime.utcnow()
    else:
        db_user.approved_at = None
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/users/{user_id}/toggle-status")
def toggle_user_status(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """切换用户状态（激活/禁用）"""
    db_user = db.query(User).filter(
        User.id == user_id,
        (User.is_deleted == False) | (User.is_deleted.is_(None))
    ).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    db_user.is_active = not db_user.is_active
    db.commit()
    
    status_text = "激活" if db_user.is_active else "禁用"
    return {"message": f"用户已{status_text}"}

@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除用户（软删除）"""
    db_user = db.query(User).filter(
        User.id == user_id,
        (User.is_deleted == False) | (User.is_deleted.is_(None))
    ).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    db_user.is_deleted = True
    db_user.deleted_at = datetime.utcnow()
    db.commit()
    
    return {"message": "用户已删除"}

# 考点管理相关路由
@app.get("/exam-points", response_model=List[ExamPointSchema])
def get_exam_points(
    province_id: int = None,
    subject: str = None,
    grade: str = None,
    semester: str = None,
    level1_point: str = None,
    level2_point: str = None,
    level3_point: str = None,
    description: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取考点列表，支持查询条件"""
    query = db.query(ExamPoint)
    
    if province_id:
        query = query.filter(ExamPoint.province_id == province_id)
    if subject:
        query = query.filter(ExamPoint.subject == subject)
    if grade:
        query = query.filter(ExamPoint.grade == grade)
    if semester:
        query = query.filter(ExamPoint.semester == semester)
    if level1_point:
        query = query.filter(ExamPoint.level1_point.contains(level1_point))
    if level2_point:
        query = query.filter(ExamPoint.level2_point.contains(level2_point))
    if level3_point:
        query = query.filter(ExamPoint.level3_point.contains(level3_point))
    if description:
        query = query.filter(ExamPoint.description.contains(description))
    
    exam_points = query.all()
    return exam_points

@app.get("/exam-points/{exam_point_id}", response_model=ExamPointSchema)
def get_exam_point(
    exam_point_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取单个考点信息"""
    exam_point = db.query(ExamPoint).filter(ExamPoint.id == exam_point_id).first()
    if not exam_point:
        raise HTTPException(status_code=404, detail="考点不存在")
    return exam_point

@app.post("/exam-points", response_model=ExamPointSchema)
def create_exam_point(
    exam_point: ExamPointCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新考点"""
    db_exam_point = ExamPoint(
        province_id=exam_point.province_id,
        subject=exam_point.subject,
        grade=exam_point.grade,
        semester=exam_point.semester,
        level1_point=exam_point.level1_point,
        level2_point=exam_point.level2_point,
        level3_point=exam_point.level3_point,
        description=exam_point.description,
        coverage_rate=int(exam_point.coverage_rate),  # 直接存储整数
        added_by=exam_point.added_by,
        is_active=exam_point.is_active
    )
    db.add(db_exam_point)
    db.commit()
    db.refresh(db_exam_point)
    return db_exam_point

@app.put("/exam-points/{exam_point_id}", response_model=ExamPointSchema)
def update_exam_point(
    exam_point_id: int,
    exam_point_update: ExamPointUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新考点信息"""
    db_exam_point = db.query(ExamPoint).filter(ExamPoint.id == exam_point_id).first()
    if not db_exam_point:
        raise HTTPException(status_code=404, detail="考点不存在")
    
    # 更新字段
    update_data = exam_point_update.dict(exclude_unset=True)
    if "coverage_rate" in update_data:
        update_data["coverage_rate"] = int(update_data["coverage_rate"])
    
    for field, value in update_data.items():
        setattr(db_exam_point, field, value)
    
    db_exam_point.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_exam_point)
    return db_exam_point

@app.delete("/exam-points/{exam_point_id}")
def delete_exam_point(
    exam_point_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除考点"""
    db_exam_point = db.query(ExamPoint).filter(ExamPoint.id == exam_point_id).first()
    if not db_exam_point:
        raise HTTPException(status_code=404, detail="考点不存在")
    
    db.delete(db_exam_point)
    db.commit()
    
    return {"message": "考点删除成功"}

@app.post("/exam-points/import")
def import_exam_points(
    import_data: ExamPointImport,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批量导入考点数据"""
    imported_count = 0
    for exam_point_data in import_data.exam_points:
        db_exam_point = ExamPoint(
            province_id=exam_point_data.province_id,
            subject=exam_point_data.subject,
            grade=exam_point_data.grade,
            semester=exam_point_data.semester,
            level1_point=exam_point_data.level1_point,
            level2_point=exam_point_data.level2_point,
            level3_point=exam_point_data.level3_point,
            description=exam_point_data.description,
            coverage_rate=int(exam_point_data.coverage_rate * 100),
            added_by=exam_point_data.added_by,
            is_active=exam_point_data.is_active
        )
        db.add(db_exam_point)
        imported_count += 1
    
    db.commit()
    return {"message": f"成功导入 {imported_count} 条考点数据", "imported_count": imported_count} 

# 初始化Ollama服务
ollama_service = OllamaService()

# 高考试题相关路由
@app.get("/exam-papers", response_model=List[ExamPaperSchema])
def get_exam_papers(
    year: int = None,
    province_id: int = None,
    subject: str = None,
    paper_name: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取高考试卷列表"""
    query = db.query(ExamPaper).filter(ExamPaper.is_active == True)
    
    if year:
        query = query.filter(ExamPaper.year == year)
    if province_id:
        query = query.filter(ExamPaper.province_id == province_id)
    if subject:
        query = query.filter(ExamPaper.subject == subject)
    if paper_name:
        query = query.filter(ExamPaper.paper_name.contains(paper_name))
    
    exam_papers = query.offset(skip).limit(limit).all()
    return [
        ExamPaperSchema(
            id=paper.id,
            year=paper.year,
            province_id=paper.province_id,
            subject=paper.subject,
            paper_name=paper.paper_name,
            file_path=paper.file_path,
            file_type=paper.file_type,
            total_score=paper.total_score,
            exam_time=paper.exam_time,
            added_by=paper.added_by,
            is_active=paper.is_active,
            province_name=paper.province.name if paper.province else None,
            created_at=paper.created_at,
            updated_at=paper.updated_at
        )
        for paper in exam_papers
    ]

@app.get("/exam-papers/{paper_id}", response_model=ExamPaperWithQuestions)
def get_exam_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取单个高考试卷详情"""
    exam_paper = db.query(ExamPaper).filter(
        ExamPaper.id == paper_id,
        ExamPaper.is_active == True
    ).first()
    
    if not exam_paper:
        raise HTTPException(status_code=404, detail="试卷不存在")
    
    return exam_paper

@app.post("/exam-papers", response_model=ExamPaperSchema)
def create_exam_paper(
    exam_paper: ExamPaperCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新高考试卷"""
    db_exam_paper = ExamPaper(
        year=exam_paper.year,
        province_id=exam_paper.province_id,
        subject=exam_paper.subject,
        paper_name=exam_paper.paper_name,
        file_path=exam_paper.file_path,
        file_type=exam_paper.file_type,
        total_score=exam_paper.total_score,
        exam_time=exam_paper.exam_time,
        added_by=exam_paper.added_by,
        is_active=exam_paper.is_active
    )
    db.add(db_exam_paper)
    db.commit()
    db.refresh(db_exam_paper)
    return db_exam_paper

@app.put("/exam-papers/{paper_id}", response_model=ExamPaperSchema)
def update_exam_paper(
    paper_id: int,
    exam_paper_update: ExamPaperUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新高考试卷"""
    db_exam_paper = db.query(ExamPaper).filter(
        ExamPaper.id == paper_id,
        ExamPaper.is_active == True
    ).first()
    
    if not db_exam_paper:
        raise HTTPException(status_code=404, detail="试卷不存在")
    
    update_data = exam_paper_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_exam_paper, field, value)
    
    db_exam_paper.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_exam_paper)
    return db_exam_paper

@app.delete("/exam-papers/{paper_id}")
def delete_exam_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除高考试卷（状态删除）"""
    db_exam_paper = db.query(ExamPaper).filter(
        ExamPaper.id == paper_id,
        ExamPaper.is_active == True
    ).first()
    
    if not db_exam_paper:
        raise HTTPException(status_code=404, detail="试卷不存在")
    
    db_exam_paper.is_active = False
    db.commit()
    
    return {"message": "试卷删除成功"}

@app.post("/exam-papers/upload", response_model=FileUploadResponse)
async def upload_exam_paper_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """上传高考试卷文件"""
    print(f"开始处理文件上传: {file.filename}")
    
    if not is_allowed_file(file.filename):
        print(f"文件类型不允许: {file.filename}")
        raise HTTPException(status_code=400, detail="不支持的文件类型")
    
    try:
        file_content = await file.read()
        print(f"文件读取成功，大小: {len(file_content)} bytes")
        
        file_path = save_uploaded_file(file_content, file.filename)
        print(f"文件保存结果: {file_path}")
        
        if not file_path:
            print("文件保存失败")
            raise HTTPException(status_code=500, detail="文件保存失败")
        
        response_data = FileUploadResponse(
            filename=file.filename,
            file_path=file_path,
            file_type=file.filename.split('.')[-1],
            message="文件上传成功"
        )
        print(f"上传成功，返回数据: {response_data}")
        return response_data
        
    except Exception as e:
        print(f"文件上传异常: {e}")
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@app.post("/exam-papers/{paper_id}/extract-questions")
def extract_questions(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """从试卷文件提取试题"""
    print(f"开始提取试题，试卷ID: {paper_id}")
    
    exam_paper = db.query(ExamPaper).filter(
        ExamPaper.id == paper_id,
        ExamPaper.is_active == True
    ).first()
    
    if not exam_paper:
        print(f"试卷不存在: {paper_id}")
        raise HTTPException(status_code=404, detail="试卷不存在")
    
    if not exam_paper.file_path:
        print(f"试卷文件不存在: {paper_id}")
        raise HTTPException(status_code=400, detail="试卷文件不存在")
    
    print(f"试卷文件路径: {exam_paper.file_path}")
    
    # 检查Ollama连接
    print("检查Ollama连接...")
    if not ollama_service.test_connection():
        print("Ollama服务连接失败")
        raise HTTPException(status_code=500, detail="Ollama服务连接失败")
    
    print("Ollama连接成功，开始提取试题...")
    
    # 使用Ollama提取试题数据
    extraction_result = ollama_service.extract_exam_data(
        exam_paper.file_path, 
        exam_paper.file_type or "unknown"
    )
    
    if not extraction_result:
        print("试题提取失败")
        raise HTTPException(status_code=500, detail="试题提取失败")
    
    print(f"提取结果: {extraction_result}")
    
    # 保存提取的试题到数据库
    created_questions = []
    questions_data = extraction_result.get('questions', [])
    
    for question_data in questions_data:
        db_question = ExamQuestion(
            exam_paper_id=paper_id,
            question_number=question_data.get('question_number', ''),
            question_type=question_data.get('question_type', '未知'),
            question_content=question_data.get('question_content', ''),
            score=question_data.get('score'),
            difficulty_level=question_data.get('difficulty_level', '中等'),
            exam_points=question_data.get('exam_points', ''),
            answer_content=question_data.get('answer_content'),
            answer_explanation=question_data.get('answer_explanation'),
            added_by=current_user.username,
            is_active=True
        )
        db.add(db_question)
        created_questions.append(db_question)
    
    db.commit()
    print(f"成功保存 {len(created_questions)} 道试题")
    
    return {
        "message": f"成功提取 {len(created_questions)} 道试题",
        "questions_count": len(created_questions),
        "extraction_result": extraction_result
    }

@app.post("/exam-papers/{paper_id}/extract-with-ollama")
def extract_questions_with_ollama(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """使用Ollama从试卷文件提取试题"""
    exam_paper = db.query(ExamPaper).filter(
        ExamPaper.id == paper_id,
        ExamPaper.is_active == True
    ).first()
    
    if not exam_paper:
        raise HTTPException(status_code=404, detail="试卷不存在")
    
    if not exam_paper.file_path:
        raise HTTPException(status_code=400, detail="试卷文件不存在")
    
    # 检查Ollama连接
    if not ollama_service.test_connection():
        raise HTTPException(status_code=500, detail="Ollama服务连接失败")
    
    # 使用Ollama提取试题数据
    extraction_result = ollama_service.extract_exam_data(
        exam_paper.file_path, 
        exam_paper.file_type or "unknown"
    )
    
    if not extraction_result:
        raise HTTPException(status_code=500, detail="试题提取失败")
    
    # 保存提取的试题到数据库
    created_questions = []
    for question_data in extraction_result.get('questions', []):
        db_question = ExamQuestion(
            exam_paper_id=paper_id,
            question_number=question_data.get('question_number', ''),
            question_type=question_data.get('question_type', '未知'),
            question_content=question_data.get('question_content', ''),
            score=question_data.get('score'),
            difficulty_level=question_data.get('difficulty_level', '中等'),
            exam_points=question_data.get('exam_points', ''),
            answer_content=question_data.get('answer_content'),
            answer_explanation=question_data.get('answer_explanation'),
            added_by=current_user.username,
            is_active=True
        )
        db.add(db_question)
        created_questions.append(db_question)
    
    db.commit()
    
    return {
        "message": f"成功提取 {len(created_questions)} 道试题",
        "questions_count": len(created_questions),
        "extraction_result": extraction_result
    }

# 试题管理相关路由
@app.get("/exam-questions", response_model=List[ExamQuestionSchema])
def get_exam_questions(
    exam_paper_id: int = None,
    question_type: str = None,
    question_number: str = None,
    difficulty_level: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取试题列表"""
    query = db.query(ExamQuestion).filter(ExamQuestion.is_active == True)
    
    if exam_paper_id:
        query = query.filter(ExamQuestion.exam_paper_id == exam_paper_id)
    if question_type:
        query = query.filter(ExamQuestion.question_type == question_type)
    if question_number:
        query = query.filter(ExamQuestion.question_number.contains(question_number))
    if difficulty_level:
        query = query.filter(ExamQuestion.difficulty_level == difficulty_level)
    
    questions = query.offset(skip).limit(limit).all()
    return questions

@app.get("/exam-questions/{question_id}", response_model=ExamQuestionSchema)
def get_exam_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取单个试题详情"""
    question = db.query(ExamQuestion).filter(
        ExamQuestion.id == question_id,
        ExamQuestion.is_active == True
    ).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="试题不存在")
    
    return question

@app.post("/exam-questions", response_model=ExamQuestionSchema)
def create_exam_question(
    exam_question: ExamQuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新试题"""
    db_question = ExamQuestion(
        exam_paper_id=exam_question.exam_paper_id,
        question_number=exam_question.question_number,
        question_type=exam_question.question_type,
        question_content=exam_question.question_content,
        score=exam_question.score,
        difficulty_level=exam_question.difficulty_level,
        exam_points=exam_question.exam_points,
        answer_content=exam_question.answer_content,
        answer_explanation=exam_question.answer_explanation,
        added_by=exam_question.added_by,
        is_active=exam_question.is_active
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@app.put("/exam-questions/{question_id}", response_model=ExamQuestionSchema)
def update_exam_question(
    question_id: int,
    exam_question_update: ExamQuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新试题"""
    db_question = db.query(ExamQuestion).filter(
        ExamQuestion.id == question_id,
        ExamQuestion.is_active == True
    ).first()
    
    if not db_question:
        raise HTTPException(status_code=404, detail="试题不存在")
    
    update_data = exam_question_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_question, field, value)
    
    db_question.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_question)
    return db_question

@app.delete("/exam-questions/{question_id}")
def delete_exam_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除试题（状态删除）"""
    db_question = db.query(ExamQuestion).filter(
        ExamQuestion.id == question_id,
        ExamQuestion.is_active == True
    ).first()
    
    if not db_question:
        raise HTTPException(status_code=404, detail="试题不存在")
    
    db_question.is_active = False
    db.commit()
    
    return {"message": "试题删除成功"}

@app.get("/files/{filename}")
def get_file(filename: str, current_user: User = Depends(get_current_user)):
    """获取上传的文件（用于预览）"""
    # 安全检查：确保文件名不包含路径遍历
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="无效的文件名")
    
    # 构建文件路径
    file_path = os.path.join("uploads", filename)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    # 根据文件类型设置正确的Content-Type
    content_type = "application/octet-stream"
    if filename.lower().endswith('.pdf'):
        content_type = "application/pdf"
    elif filename.lower().endswith(('.doc', '.docx')):
        content_type = "application/msword" if filename.lower().endswith('.doc') else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    
    return FileResponse(
        path=file_path,
        media_type=content_type,
        filename=filename
    )

# Ollama服务状态检查
@app.get("/ollama/status")
def check_ollama_status():
    """检查Ollama服务状态"""
    is_connected = ollama_service.test_connection()
    return {
        "status": "connected" if is_connected else "disconnected",
        "base_url": settings.OLLAMA_BASE_URL,
        "model": settings.OLLAMA_MODEL
    } 
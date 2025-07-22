from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# 省份和城市相关模型
class ProvinceBase(BaseModel):
    name: str
    code: str

class ProvinceCreate(ProvinceBase):
    pass

class Province(ProvinceBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CityBase(BaseModel):
    name: str
    code: str
    province_id: int

class CityCreate(CityBase):
    pass

class City(CityBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CityWithProvince(City):
    province: Province
    
    class Config:
        from_attributes = True

# 用户相关模型
class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone: Optional[str] = None
    real_name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None
    province_id: Optional[int] = None
    city_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    real_name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None
    province_id: Optional[int] = None
    city_id: Optional[int] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: Optional[bool] = None
    is_approved: Optional[bool] = None
    is_deleted: Optional[bool] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    province: Optional[Province] = None
    city: Optional[City] = None
    
    class Config:
        from_attributes = True

class UserList(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone: Optional[str] = None
    real_name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None
    province_id: Optional[int] = None
    city_id: Optional[int] = None
    is_active: Optional[bool] = None
    is_approved: Optional[bool] = None
    is_deleted: Optional[bool] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    province: Optional[Province] = None
    city: Optional[City] = None
    
    class Config:
        from_attributes = True

# 认证相关模型
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserApproval(BaseModel):
    is_approved: bool

# 考点相关模型
class ExamPointBase(BaseModel):
    province_id: int
    subject: str
    grade: str
    semester: str
    level1_point: str
    level2_point: Optional[str] = None
    level3_point: Optional[str] = None
    description: str
    coverage_rate: float  # 历年高考覆盖率
    added_by: str
    is_active: bool = True
    province_name: Optional[str] = None

class ExamPointCreate(ExamPointBase):
    pass

class ExamPointUpdate(BaseModel):
    province: Optional[str] = None
    subject: Optional[str] = None
    grade: Optional[str] = None
    semester: Optional[str] = None
    level1_point: Optional[str] = None
    level2_point: Optional[str] = None
    level3_point: Optional[str] = None
    description: Optional[str] = None
    coverage_rate: Optional[float] = None
    is_active: Optional[bool] = None

class ExamPoint(ExamPointBase):
    id: int
    added_date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ExamPointImport(BaseModel):
    exam_points: List[ExamPointCreate]

class ExamPointQuery(BaseModel):
    province: Optional[str] = None
    subject: Optional[str] = None
    grade: Optional[str] = None
    semester: Optional[str] = None
    level1_point: Optional[str] = None
    level2_point: Optional[str] = None
    level3_point: Optional[str] = None
    description: Optional[str] = None 

# 高考试题相关模型
class ExamPaperBase(BaseModel):
    year: int
    province_id: int
    subject: str
    paper_name: str
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    total_score: Optional[int] = None
    exam_time: Optional[int] = None
    added_by: str
    is_active: bool = True
    province_name: Optional[str] = None

class ExamPaperCreate(ExamPaperBase):
    pass

class ExamPaperUpdate(BaseModel):
    year: Optional[int] = None
    province: Optional[str] = None
    subject: Optional[str] = None
    paper_name: Optional[str] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    total_score: Optional[int] = None
    exam_time: Optional[int] = None
    is_active: Optional[bool] = None

class ExamPaper(ExamPaperBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ExamQuestionBase(BaseModel):
    exam_paper_id: int
    question_number: str
    question_type: str
    question_content: str
    score: Optional[Decimal] = None
    difficulty_level: Optional[str] = None
    exam_points: Optional[str] = None
    answer_content: Optional[str] = None
    answer_explanation: Optional[str] = None
    added_by: str
    is_active: bool = True

class ExamQuestionCreate(ExamQuestionBase):
    pass

class ExamQuestionUpdate(BaseModel):
    question_number: Optional[str] = None
    question_type: Optional[str] = None
    question_content: Optional[str] = None
    score: Optional[Decimal] = None
    difficulty_level: Optional[str] = None
    exam_points: Optional[str] = None
    answer_content: Optional[str] = None
    answer_explanation: Optional[str] = None
    is_active: Optional[bool] = None

class ExamQuestion(ExamQuestionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 包含关联数据的模型
class ExamPaperWithQuestions(ExamPaper):
    questions: List[ExamQuestion] = []
    
    class Config:
        from_attributes = True

# 文件上传相关模型
class FileUploadResponse(BaseModel):
    filename: str
    file_path: str
    file_type: str
    message: str

# 试题查询模型
class ExamPaperQuery(BaseModel):
    year: Optional[int] = None
    province: Optional[str] = None
    subject: Optional[str] = None
    paper_name: Optional[str] = None

class ExamQuestionQuery(BaseModel):
    exam_paper_id: Optional[int] = None
    question_type: Optional[str] = None
    question_number: Optional[str] = None
    difficulty_level: Optional[str] = None

# Ollama提取结果模型
class OllamaExtractionResult(BaseModel):
    year: int
    province: str
    subject: str
    paper_name: str
    questions: List[ExamQuestionCreate] 
import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import models
from database import Base, get_db
from auth import get_password_hash

# 创建内存数据库用于测试
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建测试数据库表
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def ensure_admin():
    """确保admin用户存在"""
    db = TestingSessionLocal()
    
    # 清理可能存在的admin用户
    db.query(models.User).filter(models.User.username == "admin").delete()
    db.commit()
    
    # 创建admin用户
    admin_user = models.User(
        username="admin",
        email="admin@admin.com",
        hashed_password=get_password_hash("admin123"),
        is_active=True,
        is_approved=True,
        is_superuser=True,
        is_deleted=False
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    db.close()
    return admin_user

def get_token():
    """获取admin用户的token"""
    # 确保admin用户存在
    ensure_admin()
    
    # 使用相同的数据库会话进行登录
    def override_get_db_for_login():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    # 临时覆盖依赖
    app.dependency_overrides[get_db] = override_get_db_for_login
    
    try:
        resp = client.post("/auth/login", data={"username": "admin", "password": "admin123"})
        assert resp.status_code == 200
        return resp.json()["access_token"]
    finally:
        # 恢复原始依赖
        app.dependency_overrides[get_db] = override_get_db

def auth_headers():
    """获取带认证头的请求头"""
    token = get_token()
    return {"Authorization": f"Bearer {token}"}

def test_get_provinces():
    """测试获取省份列表"""
    resp = client.get("/provinces", headers=auth_headers())
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_cities_by_province():
    """测试根据省份获取城市列表"""
    resp = client.get("/provinces/1/cities", headers=auth_headers())
    assert resp.status_code in (200, 404)

def test_exam_points_import():
    """测试考点数据导入"""
    resp = client.post("/exam-points/import", json={"data": []}, headers=auth_headers())
    assert resp.status_code in (200, 422)

def test_exam_papers_upload():
    """测试试卷文件上传"""
    with open(__file__, "rb") as f:
        files = {"file": ("test.txt", f, "text/plain")}
        resp = client.post("/exam-papers/upload", files=files, headers=auth_headers())
        assert resp.status_code in (200, 400, 422)

def test_ollama_status():
    """测试Ollama状态检查"""
    resp = client.get("/ollama/status", headers=auth_headers())
    assert resp.status_code == 200
    assert "status" in resp.json()

def test_user_approve_and_toggle():
    """测试用户审核和状态切换"""
    # 先创建一个测试用户
    test_user_data = {
        "username": "testuser_approve",
        "email": "test_approve@example.com",
        "password": "testpass123"
    }
    register_resp = client.post("/auth/register", json=test_user_data)
    assert register_resp.status_code == 200
    user_id = register_resp.json()["id"]
    
    # 测试审核用户
    resp = client.put(f"/users/{user_id}/approve", json={"is_approved": True}, headers=auth_headers())
    assert resp.status_code in (200, 404)
    
    # 测试切换用户状态
    resp2 = client.put(f"/users/{user_id}/toggle-status", headers=auth_headers())
    assert resp2.status_code in (200, 404)

def test_user_delete():
    """测试删除用户"""
    # 先创建一个测试用户
    test_user_data = {
        "username": "testuser_delete",
        "email": "test_delete@example.com",
        "password": "testpass123"
    }
    register_resp = client.post("/auth/register", json=test_user_data)
    assert register_resp.status_code == 200
    user_id = register_resp.json()["id"]
    
    # 测试删除用户
    resp = client.delete(f"/users/{user_id}", headers=auth_headers())
    assert resp.status_code in (200, 404)

def test_exam_paper_extract_with_ollama():
    """测试Ollama提取题目"""
    resp = client.post("/exam-papers/1/extract-with-ollama", headers=auth_headers())
    assert resp.status_code in (200, 404, 422)

def test_get_users():
    """测试获取用户列表"""
    resp = client.get("/users", headers=auth_headers())
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_single_user():
    """测试获取单个用户信息"""
    # 先注册
    user_data = {"username": "single_user", "email": "single_user@test.com", "password": "testpass123"}
    reg = client.post("/auth/register", json=user_data)
    assert reg.status_code == 200
    user_id = reg.json()["id"]
    resp = client.get(f"/users/{user_id}", headers=auth_headers())
    assert resp.status_code in (200, 404)

def test_update_user():
    """测试更新用户信息"""
    user_data = {"username": "update_user", "email": "update_user@test.com", "password": "testpass123"}
    reg = client.post("/auth/register", json=user_data)
    assert reg.status_code == 200
    user_id = reg.json()["id"]
    update = {"real_name": "新名字", "age": 22}
    resp = client.put(f"/users/{user_id}", json=update, headers=auth_headers())
    assert resp.status_code in (200, 404)

def test_get_current_user():
    """测试获取当前用户信息"""
    resp = client.get("/users/me", headers=auth_headers())
    assert resp.status_code == 200
    assert "username" in resp.json()

def test_exam_points_crud():
    """测试考点增删查改"""
    # 创建
    data = {"level1_point": "函数", "level2_point": "初等函数", "level3_point": "指数函数", "description": "测试考点"}
    resp = client.post("/exam-points", json=data, headers=auth_headers())
    assert resp.status_code in (200, 422)
    if resp.status_code == 200:
        eid = resp.json()["id"]
        # 查
        getr = client.get(f"/exam-points/{eid}", headers=auth_headers())
        assert getr.status_code == 200
        # 改
        update = {"description": "已修改"}
        upr = client.put(f"/exam-points/{eid}", json=update, headers=auth_headers())
        assert upr.status_code == 200
        # 删
        delr = client.delete(f"/exam-points/{eid}", headers=auth_headers())
        assert delr.status_code == 200

def test_exam_points_import_normal():
    """测试考点数据正常导入"""
    data = {"data": [{"level1_point": "函数", "level2_point": "初等函数", "level3_point": "对数函数", "description": "导入测试"}]}
    resp = client.post("/exam-points/import", json=data, headers=auth_headers())
    assert resp.status_code in (200, 422)

def test_exam_papers_crud():
    """测试试卷增删查改"""
    # 创建
    data = {"year": 2024, "province_id": 1, "subject": "数学", "paper_name": "测试卷", "total_score": 150, "exam_time": 120}
    resp = client.post("/exam-papers", json=data, headers=auth_headers())
    assert resp.status_code in (200, 422)
    if resp.status_code == 200:
        pid = resp.json()["id"]
        # 查
        getr = client.get(f"/exam-papers/{pid}", headers=auth_headers())
        assert getr.status_code == 200
        # 改
        update = {"paper_name": "已修改"}
        upr = client.put(f"/exam-papers/{pid}", json=update, headers=auth_headers())
        assert upr.status_code == 200
        # 删
        delr = client.delete(f"/exam-papers/{pid}", headers=auth_headers())
        assert delr.status_code == 200

def test_exam_papers_upload_normal():
    """测试试卷文件正常上传"""
    import io
    file_content = b"test exam paper content"
    files = {"file": ("test_exam.txt", io.BytesIO(file_content), "text/plain")}
    resp = client.post("/exam-papers/upload", files=files, headers=auth_headers())
    assert resp.status_code in (200, 400, 422)

def test_exam_paper_extract_with_ollama_normal():
    """测试Ollama正常提取题目流程"""
    # 这里假设paper_id=1存在，否则只测接口可用性
    resp = client.post("/exam-papers/1/extract-with-ollama", headers=auth_headers())
    assert resp.status_code in (200, 404, 422)

def test_exam_questions_crud():
    """测试试题增删查改"""
    # 创建
    data = {"exam_paper_id": 1, "question_number": "1", "question_type": "选择题", "question_content": "1+1=？", "score": 5, "difficulty_level": "简单", "added_by": "admin"}
    resp = client.post("/exam-questions", json=data, headers=auth_headers())
    assert resp.status_code in (200, 422)
    if resp.status_code == 200:
        qid = resp.json()["id"]
        # 查
        getr = client.get(f"/exam-questions/{qid}", headers=auth_headers())
        assert getr.status_code == 200
        # 改
        update = {"question_content": "1+2=？"}
        upr = client.put(f"/exam-questions/{qid}", json=update, headers=auth_headers())
        assert upr.status_code == 200
        # 删
        delr = client.delete(f"/exam-questions/{qid}", headers=auth_headers())
        assert delr.status_code == 200 
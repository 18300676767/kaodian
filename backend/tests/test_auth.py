import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import models
from database import Base, get_db
from main import app

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

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }

@pytest.fixture
def test_user(test_user_data):
    from auth import get_password_hash
    db = TestingSessionLocal()
    
    # 清理可能存在的用户
    db.query(models.User).filter(models.User.username == test_user_data["username"]).delete()
    db.commit()
    
    user = models.User(
        username=test_user_data["username"],
        email=test_user_data["email"],
        hashed_password=get_password_hash(test_user_data["password"]),
        is_active=True,
        is_approved=False,
        is_deleted=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

class TestAuthFunctions:
    def test_password_hashing(self):
        """测试密码哈希功能"""
        from auth import get_password_hash, verify_password
        
        password = "testpassword"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed)
        assert not verify_password("wrongpassword", hashed)

    def test_authenticate_user_success(self, test_user):
        """测试用户认证成功"""
        from auth import authenticate_user
        db = TestingSessionLocal()
        
        user = authenticate_user(db, "testuser", "testpass123")
        assert user is not None
        assert user.username == "testuser"
        
        db.close()

    def test_authenticate_user_wrong_password(self, test_user):
        """测试用户认证失败 - 错误密码"""
        from auth import authenticate_user
        db = TestingSessionLocal()
        
        user = authenticate_user(db, "testuser", "wrongpassword")
        assert user is False
        
        db.close()

    def test_authenticate_user_nonexistent(self):
        """测试用户认证失败 - 用户不存在"""
        from auth import authenticate_user
        db = TestingSessionLocal()
        
        user = authenticate_user(db, "nonexistent", "password")
        assert user is False
        
        db.close()

    def test_create_access_token(self):
        """测试创建访问令牌"""
        from auth import create_access_token
        from datetime import timedelta
        
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)

class TestAuthAPI:
    def test_register_success(self, client, test_user_data):
        """测试用户注册成功"""
        # 清理可能存在的用户
        db = TestingSessionLocal()
        db.query(models.User).filter(models.User.username == test_user_data["username"]).delete()
        db.commit()
        db.close()
        
        response = client.post("/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == test_user_data["username"]
        assert data["email"] == test_user_data["email"]
        assert "id" in data

    def test_register_duplicate_username(self, client, test_user, test_user_data):
        """测试注册重复用户名"""
        response = client.post("/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "用户名已存在" in data["detail"]

    def test_register_duplicate_email(self, client, test_user):
        """测试注册重复邮箱"""
        duplicate_data = {
            "username": "newuser",
            "email": "test@example.com",  # 重复邮箱
            "password": "newpass123"
        }
        response = client.post("/auth/register", json=duplicate_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "邮箱已存在" in data["detail"]

    def test_login_success(self, client, test_user):
        """测试用户登录成功"""
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = client.post("/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user):
        """测试登录失败 - 错误密码"""
        login_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, client):
        """测试登录失败 - 用户不存在"""
        login_data = {
            "username": "nonexistent",
            "password": "password"
        }
        response = client.post("/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_success(self, client, test_user):
        """测试获取当前用户信息成功"""
        # 先登录获取token
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        login_response = client.post("/auth/login", data=login_data)
        token = login_response.json()["access_token"]
        
        # 使用token获取用户信息
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/users/me", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "testuser"

    def test_get_current_user_invalid_token(self, client):
        """测试获取当前用户信息失败 - 无效token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/users/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_no_token(self, client):
        """测试获取当前用户信息失败 - 无token"""
        response = client.get("/users/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

class TestHealthCheck:
    def test_health_check(self, client):
        """测试健康检查接口"""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "高考考点分析系统API运行正常" in data["message"]

    def test_root_endpoint(self, client):
        """测试根接口"""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND 
import os
from typing import Optional

class Settings:
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://admin:111111@localhost:3306/kaodian"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Ollama配置
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "qwen2.5:7b"  # 或其他适合的模型
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: set = {'.xlsx', '.xls', '.docx', '.doc', '.pdf', '.md', '.txt'}
    
    # 文件处理配置
    SUPPORTED_QUESTION_TYPES: set = {
        '选择题', '填空题', '解答题', '计算题', '简答题', 
        '材料分析题', '论述题', '作文题', '实验题', '改错题', '语段阅读题'
    }
    
    # 科目配置
    SUPPORTED_SUBJECTS: set = {
        '数学', '语文', '英语', '物理', '化学', '生物', 
        '历史', '地理', '政治', '文综', '理综'
    }
    
    # 省份配置
    SUPPORTED_PROVINCES: set = {
        '北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江',
        '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南',
        '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州',
        '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆'
    }

# 创建全局配置实例
settings = Settings()

# 环境变量覆盖配置
def load_config_from_env():
    """从环境变量加载配置"""
    settings.OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", settings.OLLAMA_BASE_URL)
    settings.OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", settings.OLLAMA_MODEL)
    settings.DATABASE_URL = os.getenv("DATABASE_URL", settings.DATABASE_URL)
    settings.SECRET_KEY = os.getenv("SECRET_KEY", settings.SECRET_KEY) 
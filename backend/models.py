from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

class Province(Base):
    __tablename__ = "provinces"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    code = Column(String(10), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联城市
    cities = relationship("City", back_populates="province")

class City(Base):
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    code = Column(String(10), unique=True, index=True, nullable=False)
    province_id = Column(Integer, ForeignKey("provinces.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联省份
    province = relationship("Province", back_populates="cities")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)  # 强制不可为空
    phone = Column(String(20))
    real_name = Column(String(50))
    age = Column(Integer)
    grade = Column(String(20))
    province_id = Column(Integer, ForeignKey("provinces.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))
    is_active = Column(Boolean, default=True, nullable=True)  # 允许NULL
    is_approved = Column(Boolean, default=False, nullable=True)  # 允许NULL
    is_deleted = Column(Boolean, default=False, nullable=True)  # 允许NULL
    is_superuser = Column(Boolean, default=False, nullable=True)  # 超级用户标识
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    approved_at = Column(DateTime(timezone=True))
    deleted_at = Column(DateTime(timezone=True))
    
    # 关联省份和城市
    province = relationship("Province")
    city = relationship("City")

class ExamPoint(Base):
    __tablename__ = "exam_points"
    
    id = Column(Integer, primary_key=True, index=True)
    province_id = Column(Integer, ForeignKey("provinces.id"), nullable=False)
    subject = Column(String(50), nullable=False, index=True)
    grade = Column(String(20), nullable=False, index=True)
    semester = Column(String(20), nullable=False, index=True)
    level1_point = Column(String(100), nullable=False, index=True)
    level2_point = Column(String(100), nullable=True, index=True)
    level3_point = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=False)
    coverage_rate = Column(Integer, nullable=False)  # 历年高考覆盖率，存储为整数（百分比）
    added_by = Column(String(50), nullable=False)
    added_date = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# 高考试题相关模型
class ExamPaper(Base):
    """高考试卷表"""
    __tablename__ = "exam_papers"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)  # 年份
    province_id = Column(Integer, ForeignKey("provinces.id"), nullable=False)
    subject = Column(String(50), nullable=False, index=True)  # 科目
    paper_name = Column(String(200), nullable=False)  # 试卷名称
    file_path = Column(String(500), nullable=True)  # 文件路径
    file_type = Column(String(20), nullable=True)  # 文件类型 (excel, word, pdf, md)
    total_score = Column(Integer, nullable=True)  # 总分
    exam_time = Column(Integer, nullable=True)  # 考试时长(分钟)
    added_by = Column(String(50), nullable=False)  # 添加人
    is_active = Column(Boolean, default=True, nullable=False)  # 状态删除
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联试题
    questions = relationship("ExamQuestion", back_populates="exam_paper")
    province = relationship("Province")

class ExamQuestion(Base):
    """高考试题表"""
    __tablename__ = "exam_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    exam_paper_id = Column(Integer, ForeignKey("exam_papers.id"), nullable=False)
    question_number = Column(String(20), nullable=False)  # 题号
    question_type = Column(String(50), nullable=False, index=True)  # 题目类型
    question_content = Column(Text, nullable=False)  # 题目内容
    score = Column(DECIMAL(5,2), nullable=True)  # 分值
    difficulty_level = Column(String(20), nullable=True)  # 难度等级
    exam_points = Column(Text, nullable=True)  # 相关考点
    answer_content = Column(Text, nullable=True)  # 参考答案
    answer_explanation = Column(Text, nullable=True)  # 答案解析
    added_by = Column(String(50), nullable=False)  # 添加人
    is_active = Column(Boolean, default=True, nullable=False)  # 状态删除
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联试卷
    exam_paper = relationship("ExamPaper", back_populates="questions") 
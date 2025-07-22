import os
import uuid
from datetime import datetime
from typing import Optional, List, Dict
import pandas as pd
from docx import Document
import PyPDF2
import re
from config import settings

# 文件上传配置
UPLOAD_DIR = settings.UPLOAD_DIR
ALLOWED_EXTENSIONS = settings.ALLOWED_EXTENSIONS

def ensure_upload_dir():
    """确保上传目录存在"""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    return UPLOAD_DIR

def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    return os.path.splitext(filename)[1].lower()

def is_allowed_file(filename: str) -> bool:
    """检查文件类型是否允许"""
    return get_file_extension(filename) in ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename: str) -> str:
    """生成唯一的文件名"""
    ext = get_file_extension(original_filename)
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{unique_id}{ext}"

def save_uploaded_file(file_content: bytes, filename: str) -> Optional[str]:
    """保存上传的文件"""
    try:
        ensure_upload_dir()
        
        if not is_allowed_file(filename):
            return None
            
        unique_filename = generate_unique_filename(filename)
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, 'wb') as f:
            f.write(file_content)
            
        return file_path
    except Exception as e:
        print(f"保存文件失败: {e}")
        return None

def extract_text_from_pdf(file_path: str) -> str:
    """从PDF文件提取文本"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"PDF文本提取失败: {e}")
        return ""

def extract_text_from_word(file_path: str) -> str:
    """从Word文件提取文本"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Word文本提取失败: {e}")
        return ""

def extract_text_from_excel(file_path: str) -> str:
    """从Excel文件提取文本"""
    try:
        df = pd.read_excel(file_path)
        text = df.to_string(index=False)
        return text
    except Exception as e:
        print(f"Excel文本提取失败: {e}")
        return ""

def extract_text_from_markdown(file_path: str) -> str:
    """从Markdown文件提取文本"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Markdown文本提取失败: {e}")
        return ""

def extract_text_from_file(file_path: str) -> str:
    """根据文件类型提取文本内容"""
    ext = get_file_extension(file_path)
    
    if ext in ['.xlsx', '.xls']:
        return extract_text_from_excel(file_path)
    elif ext in ['.docx', '.doc']:
        return extract_text_from_word(file_path)
    elif ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext in ['.md', '.txt']:
        return extract_text_from_markdown(file_path)
    else:
        return "" 
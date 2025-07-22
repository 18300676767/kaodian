import requests
import json
import base64
from typing import List, Dict, Optional
from config import settings
import logging

logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        
    def _make_request(self, endpoint: str, data: Optional[dict] = None, files: Optional[dict] = None) -> Optional[dict]:
        """发送请求到Ollama"""
        try:
            url = f"{self.base_url}{endpoint}"
            if files:
                response = requests.post(url, files=files, timeout=1800)
            else:
                response = requests.post(url, json=data, timeout=1800)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Ollama请求失败: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Ollama服务连接失败: {e}")
            return None
    
    def extract_exam_data(self, file_path: str, file_type: str) -> Optional[Dict]:
        """从文件提取试题数据"""
        try:
            print(f"开始提取试题数据，文件路径: {file_path}, 文件类型: {file_type}")
            
            # 读取文件内容
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            print(f"文件读取成功，大小: {len(file_content)} bytes")
            
            # 尝试提取文本内容
            text_content = self._extract_text_from_file(file_content, file_type)
            if not text_content:
                print("无法提取文本内容")
                return None
            
            print(f"提取的文本内容长度: {len(text_content)} 字符")
            
            # 构建提示词
            prompt = self._build_extraction_prompt_with_content(file_type, text_content)
            print(f"构建提示词完成")
            
            # 发送到Ollama
            data = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9
                }
            }
            
            print(f"发送请求到Ollama，模型: {self.model}")
            response = self._make_request("/api/generate", data=data)
            
            if response and 'response' in response:
                print(f"Ollama返回响应: {response['response'][:200]}...")
                # 解析Ollama返回的JSON数据
                return self._parse_extraction_result(response['response'])
            else:
                print(f"Ollama返回数据格式错误: {response}")
                logger.error("Ollama返回数据格式错误")
                return None
                
        except Exception as e:
            print(f"提取试题数据失败: {e}")
            logger.error(f"提取试题数据失败: {e}")
            return None
    
    def _extract_text_from_file(self, file_content: bytes, file_type: str) -> Optional[str]:
        """从文件中提取文本内容"""
        try:
            if file_type.lower() in ['txt', 'md']:
                # 纯文本文件
                return file_content.decode('utf-8', errors='ignore')
            elif file_type.lower() in ['docx', 'doc']:
                # Word文档，尝试简单提取
                try:
                    import docx
                    from io import BytesIO
                    doc = docx.Document(BytesIO(file_content))
                    text = []
                    for paragraph in doc.paragraphs:
                        text.append(paragraph.text)
                    return '\n'.join(text)
                except ImportError:
                    print("python-docx库未安装，无法处理Word文档")
                    return None
            elif file_type.lower() in ['pdf']:
                # PDF文件
                try:
                    import PyPDF2
                    from io import BytesIO
                    pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
                    text = []
                    for page in pdf_reader.pages:
                        text.append(page.extract_text())
                    return '\n'.join(text)
                except ImportError:
                    print("PyPDF2库未安装，无法处理PDF文件")
                    return None
            else:
                print(f"不支持的文件类型: {file_type}")
                return None
        except Exception as e:
            print(f"提取文本内容失败: {e}")
            return None

    def _build_extraction_prompt(self, file_type: str) -> str:
        """构建提取提示词"""
        return f"""
请从上传的{file_type}文件中提取高考试题信息，要求：

1. 提取试卷基本信息：
   - 年份
   - 省份
   - 科目

2. 提取每道试题的详细信息：
   - 题号
   - 题目类型（选择题、填空题、解答题/计算题、简答题、材料分析题、论述题、作文题、实验题、改错题、语段阅读题）
   - 题目内容
   - 分值
   - 相关考点
   - 参考答案（如果有）
   - 答案解析（如果有）

3. 返回格式为JSON数组，每个试题为一个对象：
{{
    "year": 年份,
    "province": "省份",
    "subject": "科目",
    "paper_name": "试卷名称",
    "questions": [
        {{
            "question_number": "题号",
            "question_type": "题目类型",
            "question_content": "题目内容",
            "score": 分值,
            "exam_points": "相关考点",
            "answer_content": "参考答案",
            "answer_explanation": "答案解析"
        }}
    ]
}}

请确保提取的信息准确完整，如果某些信息无法提取，请标记为null。
"""

    def _build_extraction_prompt_with_content(self, file_type: str, text_content: str) -> str:
        """构建包含文件内容的提取提示词"""
        return f"""
请从以下{file_type}文件内容中提取高考试题信息，务必包含所有题型（包括选择题、填空题、判断题、解答题等），不要遗漏任何题目。对于选择题，请按如下格式输出：

文件内容：
{text_content}

要求：

1. 提取试卷基本信息：
   - 年份
   - 省份
   - 科目

2. 提取每道试题的详细信息：
   - 题号
   - 题目类型（选择题、填空题、解答题/计算题、简答题、材料分析题、论述题、作文题、实验题、改错题、语段阅读题、判断题等）
   - 题目内容
   - 分值
   - 相关考点
   - 参考答案（如果有）
   - 答案解析（如果有）

3. 请严格按照以下JSON格式返回，不要添加任何额外的markdown标记或说明文字：

{
    "year": 年份,
    "province": "省份",
    "subject": "科目",
    "paper_name": "试卷名称",
    "questions": [
        {
            "question_number": "1",
            "question_type": "选择题",
            "question_content": "下列哪个选项...",
            "score": 5,
            "exam_points": "...",
            "answer_content": "A",
            "answer_explanation": "..."
        },
        {
            "question_number": "2",
            "question_type": "解答题/计算题",
            "question_content": "...",
            "score": 10,
            "exam_points": "...",
            "answer_content": "...",
            "answer_explanation": "..."
        }
        // ... 其他题目 ...
    ]
}

重要提示：
- 请确保返回的是纯JSON格式，不要包含```json或```标记
- 如果某些信息无法提取，请使用null值
- 确保JSON格式正确，没有多余的转义字符
- 字符串值请使用双引号包围
- 题型必须全面，不能遗漏选择题、填空题、判断题等客观题
"""
    
    def _get_mime_type(self, file_type: str) -> str:
        """获取文件MIME类型"""
        mime_types = {
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'xls': 'application/vnd.ms-excel',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'doc': 'application/msword',
            'pdf': 'application/pdf',
            'md': 'text/markdown',
            'txt': 'text/plain'
        }
        return mime_types.get(file_type.lower(), 'application/octet-stream')
    
    def _parse_extraction_result(self, response_text: str) -> Optional[Dict]:
        """解析Ollama返回的提取结果"""
        try:
            # 清理响应文本，移除可能的markdown代码块标记
            cleaned_text = response_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith('```'):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()
            
            # 仅移除非法ASCII控制字符，允许题干、答案等内容中保留换行
            import re
            cleaned_text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', cleaned_text)
            # 不再将裸\n、\r、\t替换为转义，直接解析
            # cleaned_text = cleaned_text.replace('\r', '\\r').replace('\n', '\\n').replace('\t', '\\t')
            
            # 尝试从响应中提取JSON
            json_start = cleaned_text.find('{')
            json_end = cleaned_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = cleaned_text[json_start:json_end]
                
                # 尝试修复常见的JSON格式问题
                json_str = json_str.replace('\\"', '"')  # 修复转义的双引号
                # 不再做如下还原！
                # json_str = json_str.replace('\\n', '\n')  # 修复换行符
                # json_str = json_str.replace('\\t', '\t')  # 修复制表符
                
                try:
                    data = json.loads(json_str)
                except json.JSONDecodeError:
                    # 如果还是失败，尝试更宽松的解析
                    import re
                    # 移除所有转义字符
                    json_str = re.sub(r'\\(.)', r'\1', json_str)
                    data = json.loads(json_str)
                
                # 验证数据结构
                if 'questions' in data and isinstance(data['questions'], list):
                    return data
                else:
                    logger.error("Ollama返回的数据结构不正确")
                    return None
            else:
                logger.error("无法从Ollama响应中提取JSON")
                return None
                
        except json.JSONDecodeError as e:
            logger.error(f"解析Ollama响应JSON失败: {e}")
            logger.error(f"原始响应: {response_text[:500]}...")
            return None
        except Exception as e:
            logger.error(f"解析提取结果失败: {e}")
            return None
    
    def test_connection(self) -> bool:
        """测试Ollama连接"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama连接测试失败: {e}")
            return False 
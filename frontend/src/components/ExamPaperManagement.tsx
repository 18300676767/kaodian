import React, { useState, useEffect } from 'react';
import { User } from '../services/api';

interface ExamPaper {
  id: number;
  year: number;
  province_id: number;
  province_name?: string;
  subject: string;
  paper_name: string;
  file_path?: string;
  file_type?: string;
  total_score?: number;
  exam_time?: number;
  added_by: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

interface ExamQuestion {
  id: number;
  exam_paper_id: number;
  question_number: string;
  question_type: string;
  question_content: string;
  score?: number;
  difficulty_level?: string;
  exam_points?: string;
  answer_content?: string;
  answer_explanation?: string;
  added_by: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  answers?: ExamAnswer[];
}

interface ExamAnswer {
  id: number;
  question_id: number;
  answer_type: string;
  answer_content: string;
  is_correct: boolean;
  explanation?: string;
  added_by: string;
  created_at: string;
  updated_at?: string;
}

interface ExamPaperManagementProps {
  currentUser: User;
}

const ExamPaperManagement: React.FC<ExamPaperManagementProps> = ({ currentUser }) => {
  const [examPapers, setExamPapers] = useState<ExamPaper[]>([]);
  const [loading, setLoading] = useState(false);
  const [currentView, setCurrentView] = useState<'papers' | 'questions'>('papers');
  const [selectedPaper, setSelectedPaper] = useState<ExamPaper | null>(null);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [showAddPaperModal, setShowAddPaperModal] = useState(false);
  const [showPreviewModal, setShowPreviewModal] = useState(false);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [provinces, setProvinces] = useState<{id:number, name:string}[]>([]);

  // 试题相关状态
  const [questions, setQuestions] = useState<ExamQuestion[]>([]);
  const [questionsLoading, setQuestionsLoading] = useState(false);

  // 表单状态
  const [paperForm, setPaperForm] = useState({
    year: new Date().getFullYear(),
    province_id: 0,
    subject: '',
    paper_name: '',
    total_score: 0,
    exam_time: 0
  });

  const [questionForm, setQuestionForm] = useState({
    question_number: '',
    question_type: '',
    question_content: '',
    score: 0,
    difficulty_level: '中等',
    exam_points: ''
  });

  const [answerForm, setAnswerForm] = useState({
    answer_type: 'text',
    answer_content: '',
    is_correct: true,
    explanation: ''
  });

  // 获取试卷列表
  const fetchExamPapers = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/exam-papers', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response && response.ok) {
        const data = await response.json();
        setExamPapers(data);
      } else {
        console.error('获取试卷列表失败:', response?.status, response?.statusText);
      }
    } catch (error) {
      console.error('获取试卷列表失败:', error);
    } finally {
      setLoading(false);
    }
  };

  // 获取试题列表
  const fetchQuestions = async (paperId: number) => {
    console.log('fetchQuestions called', paperId);
    setQuestionsLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/exam-papers/${paperId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      console.log('fetchQuestions response', response);
      if (response && response.ok) {
        const data = await response.json();
        console.log('fetchQuestions data', data);
        setQuestions(data.questions || []);
      } else {
        console.error('获取试题列表失败:', response?.status, response?.statusText);
        setQuestions([]);
      }
    } catch (error) {
      console.error('获取试题列表失败:', error);
      setQuestions([]);
    } finally {
      setQuestionsLoading(false);
    }
  };

  useEffect(() => {
    fetchExamPapers();
    
    const loadProvinces = async () => {
      try {
        // 直接请求后端接口，避免依赖代理
        const res = await fetch('http://localhost:8000/provinces', {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        
        if (!res || !res.ok) {
          const errMsg = `❌ 获取省份列表失败，请检查后端服务和登录状态！\n后端响应: ${res ? await res.text() : '无响应'}`;
          alert(errMsg);
          console.error('省份接口响应异常', res?.status, res?.statusText, errMsg);
          setProvinces([]);
          return;
        }
        
        const data = await res.json();
        setProvinces(data);
        if (Array.isArray(data) && data.length === 0) {
          alert('⚠️ 省份列表为空，请先在数据库导入省份基础数据！');
        }
      } catch (err) {
        setProvinces([]);
        alert(`❌ 获取省份列表异常，请检查网络和后端日志！\n前端异常: ${err}`);
        console.error('省份接口请求异常', err);
      }
    };
    
    loadProvinces();
  }, []);

  // 上传试卷文件
  const handleFileUpload = async () => {
    if (!uploadFile) return;

    const formData = new FormData();
    formData.append('file', uploadFile);

    try {
      const response = await fetch('http://localhost:8000/exam-papers/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        alert('✅ 文件上传成功');
        setShowUploadModal(false);
        setUploadFile(null);
        fetchExamPapers();
      } else {
        alert('❌ 文件上传失败');
      }
    } catch (error) {
      console.error('上传失败:', error);
      alert('❌ 文件上传失败');
    }
  };

  // 创建试卷
  const handleCreatePaper = async () => {
    try {
      const response = await fetch('http://localhost:8000/exam-papers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          ...paperForm,
          added_by: currentUser.username
        })
      });

      if (response.ok) {
        alert('✅ 试卷创建成功');
        setPaperForm({
          year: new Date().getFullYear(),
          province_id: 0,
          subject: '',
          paper_name: '',
          total_score: 0,
          exam_time: 0
        });
        fetchExamPapers();
      } else {
        const errMsg = `❌ 试卷创建失败\n后端响应: ${await response.text()}`;
        alert(errMsg);
        console.error('试卷创建失败', errMsg);
      }
    } catch (error) {
      console.error('创建失败:', error);
      alert(`❌ 试卷创建失败\n前端异常: ${error}`);
    }
  };

  // 创建试卷（带文件上传）
  const handleCreatePaperWithFile = async () => {
    try {
      // 如果有文件，先上传文件
      let filePath = null;
      let fileType = null;
      
      if (uploadFile) {
        const formData = new FormData();
        formData.append('file', uploadFile);

        console.log('开始上传文件:', uploadFile.name);
        const uploadResponse = await fetch('http://localhost:8000/exam-papers/upload', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: formData
        });

        console.log('上传响应状态:', uploadResponse.status);
        if (uploadResponse.ok) {
          const uploadData = await uploadResponse.json();
          console.log('上传成功，返回数据:', uploadData);
          filePath = uploadData.file_path;
          fileType = uploadData.file_type;
        } else {
          const errorText = await uploadResponse.text();
          console.error('文件上传失败:', uploadResponse.status, errorText);
          alert(`❌ 文件上传失败\n状态: ${uploadResponse.status}\n错误: ${errorText}`);
          return;
        }
      }

      // 创建试卷记录
      console.log('开始创建试卷记录:', { ...paperForm, file_path: filePath, file_type: fileType });
      const response = await fetch('http://localhost:8000/exam-papers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          ...paperForm,
          file_path: filePath,
          file_type: fileType,
          added_by: currentUser.username
        })
      });

      console.log('创建试卷响应状态:', response.status);
      if (response.ok) {
        alert('✅ 试卷创建成功');
        setPaperForm({
          year: new Date().getFullYear(),
          province_id: 0,
          subject: '',
          paper_name: '',
          total_score: 0,
          exam_time: 0
        });
        setUploadFile(null);
        fetchExamPapers();
      } else {
        const errMsg = `❌ 试卷创建失败\n后端响应: ${await response.text()}`;
        alert(errMsg);
        console.error('试卷创建失败', errMsg);
      }
    } catch (error) {
      console.error('创建失败:', error);
      alert(`❌ 试卷创建失败\n前端异常: ${error}`);
    }
  };

  // 删除试卷
  const handleDeletePaper = async (paperId: number) => {
    // eslint-disable-next-line no-restricted-globals
    if (confirm('确定要删除该试卷吗？')) {
      try {
        const response = await fetch(`http://localhost:8000/exam-papers/${paperId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.ok) {
          alert('✅ 试卷删除成功');
          fetchExamPapers();
        } else {
          alert('❌ 试卷删除失败');
        }
      } catch (error) {
        console.error('删除失败:', error);
        alert('❌ 试卷删除失败');
      }
    }
  };

  // 预览试卷文件
  const handlePreviewPaper = (paper: ExamPaper) => {
    if (!paper.file_path) {
      alert('❌ 该试卷没有上传文件');
      return;
    }
    setSelectedPaper(paper);
    setShowPreviewModal(true);
  };

  // 提取试题
  const handleExtractQuestions = async (paperId: number) => {
    try {
      const response = await fetch(`http://localhost:8000/exam-papers/${paperId}/extract-questions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        alert(`✅ 成功提取 ${data.questions_count} 道试题`);
        // fetchQuestions(paperId); // 已移除fetchQuestions，暂时注释
      } else {
        alert('❌ 试题提取失败');
      }
    } catch (error) {
      console.error('提取失败:', error);
      alert('❌ 试题提取失败');
    }
  };

  const renderPaperList = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">高考试卷管理</h2>
        <div className="space-x-2">
          <button
            onClick={() => setShowUploadModal(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
          >
            上传试卷
          </button>
          <button
            onClick={() => setShowAddPaperModal(true)}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md"
          >
            添加试卷
          </button>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-8">
          <div className="animate-spin h-8 w-8 border-4 border-indigo-600 border-t-transparent rounded-full mx-auto"></div>
          <p className="mt-2 text-gray-600">加载中...</p>
        </div>
      ) : (
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          {/* 查询条件区域 */}
          <div className="p-4 flex space-x-4 border-b">
            <input className="border px-2 py-1 rounded" placeholder="试卷名称" />
            <select
              value={paperForm.province_id}
              onChange={e => setPaperForm({ ...paperForm, province_id: Number(e.target.value) })}
              className="w-full border px-2 py-1 rounded"
              disabled={provinces.length === 0}
            >
              <option value="">{provinces.length === 0 ? '无可选省份，请先导入数据' : '请选择省份'}</option>
              {provinces.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
            <input className="border px-2 py-1 rounded" placeholder="科目" />
            <button className="bg-gray-200 px-3 py-1 rounded">查询</button>
          </div>
          {/* 表头 */}
          <div className="grid grid-cols-8 gap-2 px-6 py-2 bg-gray-50 text-gray-700 text-sm font-semibold">
            <div>试卷名称</div>
            <div>年份</div>
            <div>省份</div>
            <div>科目</div>
            <div>总分</div>
            <div>时长</div>
            <div>添加日期</div>
            <div>操作</div>
          </div>
          <ul className="divide-y divide-gray-200">
            {examPapers.length === 0 ? (
              <li className="px-6 py-8 text-center text-gray-400">暂无数据</li>
            ) : (
              examPapers.map((paper) => (
                <li key={paper.id} className="grid grid-cols-8 gap-2 px-6 py-4 items-center">
                  <div>{paper.paper_name}</div>
                  <div>{paper.year}</div>
                  <div>{paper.province_name || '-'}</div>
                  <div>{paper.subject}</div>
                  <div>{paper.total_score ?? '-'}</div>
                  <div>{paper.exam_time ?? '-'}</div>
                  <div>{paper.created_at ? new Date(paper.created_at).toLocaleDateString('zh-CN') : '-'}</div>
                  <div className="flex space-x-2">
                    <button onClick={() => handlePreviewPaper(paper)} className="text-blue-600 hover:text-blue-900 text-sm font-medium">预览试卷</button>
                    <button onClick={() => { 
                      console.log('点击查看试题', paper);
                      setSelectedPaper(paper); 
                      setCurrentView('questions'); 
                      fetchQuestions(paper.id);
                    }} className="text-indigo-600 hover:text-indigo-900 text-sm font-medium">查看试题</button>
                    <button onClick={() => handleExtractQuestions(paper.id)} className="text-green-600 hover:text-green-900 text-sm font-medium">提取试题</button>
                    <button onClick={() => handleDeletePaper(paper.id)} className="text-red-600 hover:text-red-900 text-sm font-medium">删除</button>
                  </div>
                </li>
              ))
            )}
          </ul>
        </div>
      )}
    </div>
  );

  // 上传试卷弹窗
  const renderUploadModal = () => (
    showUploadModal && (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
        <div className="bg-white p-6 rounded shadow-md w-96">
          <h3 className="text-lg font-bold mb-4">上传试卷文件</h3>
          <input
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={e => setUploadFile(e.target.files?.[0] || null)}
            className="mb-4"
          />
          <div className="flex justify-end space-x-2">
            <button
              onClick={() => setShowUploadModal(false)}
              className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
            >取消</button>
            <button
              onClick={handleFileUpload}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              disabled={!uploadFile}
            >上传</button>
          </div>
        </div>
      </div>
    )
  );

  // 添加试卷弹窗
  const renderAddPaperModal = () => (
    showAddPaperModal && (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
        <div className="bg-white p-6 rounded shadow-md w-96">
          <h3 className="text-lg font-bold mb-4">添加试卷信息</h3>
          <div className="space-y-2">
            <input
              type="number"
              placeholder="年份"
              value={paperForm.year}
              onChange={e => setPaperForm({ ...paperForm, year: Number(e.target.value) })}
              className="w-full border px-2 py-1 rounded"
            />
            <select
              value={paperForm.province_id}
              onChange={e => setPaperForm({ ...paperForm, province_id: Number(e.target.value) })}
              className="w-full border px-2 py-1 rounded"
            >
              <option value="">请选择省份</option>
              {provinces.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
            <input
              type="text"
              placeholder="科目"
              value={paperForm.subject}
              onChange={e => setPaperForm({ ...paperForm, subject: e.target.value })}
              className="w-full border px-2 py-1 rounded"
            />
            <input
              type="text"
              placeholder="试卷名称"
              value={paperForm.paper_name}
              onChange={e => setPaperForm({ ...paperForm, paper_name: e.target.value })}
              className="w-full border px-2 py-1 rounded"
            />
            <div className="flex items-center space-x-2">
              <input
                type="number"
                min={1}
                placeholder="如：150"
                value={paperForm.total_score}
                onChange={e => setPaperForm({ ...paperForm, total_score: Number(e.target.value) })}
                className="w-full border px-2 py-1 rounded"
              />
              <span className="text-gray-500">分</span>
            </div>
            <div className="flex items-center space-x-2">
              <input
                type="number"
                min={1}
                placeholder="如：120"
                value={paperForm.exam_time}
                onChange={e => setPaperForm({ ...paperForm, exam_time: Number(e.target.value) })}
                className="w-full border px-2 py-1 rounded"
              />
              <span className="text-gray-500">分钟</span>
            </div>
            
            {/* 文件上传区域 */}
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
              <div className="text-sm text-gray-600 mb-2">
                上传试卷文件 (支持 PDF、Word 格式)
              </div>
              <input
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={e => setUploadFile(e.target.files?.[0] || null)}
                className="hidden"
                id="paper-file-upload"
              />
              <label
                htmlFor="paper-file-upload"
                className="cursor-pointer bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 inline-block"
                style={{ marginBottom: 0 }}
              >
                选择文件
              </label>
              {uploadFile && (
                <div className="mt-2 text-sm text-green-600">
                  ✅ 已选择: {uploadFile.name}
                </div>
              )}
            </div>
          </div>
          <div className="flex justify-end space-x-2 mt-4">
            <button
              onClick={() => {
                setShowAddPaperModal(false);
                setUploadFile(null);
              }}
              className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
            >取消</button>
            <button
              onClick={() => { handleCreatePaperWithFile(); setShowAddPaperModal(false); }}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            >添加</button>
          </div>
        </div>
      </div>
    )
  );

  // 预览试卷弹窗
  const renderPreviewModal = () => (
    showPreviewModal && selectedPaper && (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
        <div className="bg-white rounded-lg shadow-lg w-11/12 h-5/6 flex flex-col">
          <div className="flex justify-between items-center p-4 border-b">
            <h3 className="text-lg font-bold">预览试卷：{selectedPaper.paper_name}</h3>
            <button
              onClick={() => setShowPreviewModal(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div className="flex-1 p-4">
            {selectedPaper.file_path && (
              <div className="w-full h-full">
                {selectedPaper.file_type === 'pdf' ? (
                  <iframe
                    src={`http://localhost:8000/files/${selectedPaper.file_path.split('/').pop()}?token=${localStorage.getItem('token')}`}
                    className="w-full h-full border-0"
                    title="试卷预览"
                  />
                ) : (
                  <div className="flex items-center justify-center h-full">
                    <div className="text-center">
                      <div className="text-gray-500 mb-4">
                        <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                      <p className="text-gray-600 mb-4">Word文档不支持在线预览</p>
                      <a
                        href={`http://localhost:8000/files/${selectedPaper.file_path.split('/').pop()}?token=${localStorage.getItem('token')}`}
                        download
                        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                      >
                        下载文件
                      </a>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    )
  );

  // 试题列表渲染
  const renderQuestionsList = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setCurrentView('papers')}
            className="text-blue-600 hover:text-blue-800 font-medium"
          >
            ← 返回试卷列表
          </button>
          <h2 className="text-2xl font-bold text-gray-900">
            {selectedPaper?.paper_name} - 试题列表
          </h2>
        </div>
        <div className="space-x-2">
          <button
            onClick={() => selectedPaper && handleExtractQuestions(selectedPaper.id)}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md"
          >
            重新提取试题
          </button>
        </div>
      </div>

      {questionsLoading ? (
        <div className="text-center py-8">
          <div className="animate-spin h-8 w-8 border-4 border-indigo-600 border-t-transparent rounded-full mx-auto"></div>
          <p className="mt-2 text-gray-600">加载试题中...</p>
        </div>
      ) : (
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          {questions.length === 0 ? (
            <div className="px-6 py-8 text-center text-gray-400">
              <div className="mb-4">
                <svg className="w-16 h-16 mx-auto text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <p className="text-lg font-medium mb-2">暂无试题</p>
              <p className="text-sm text-gray-500 mb-4">该试卷还没有提取试题，请点击"重新提取试题"按钮</p>
              <button
                onClick={() => selectedPaper && handleExtractQuestions(selectedPaper.id)}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
              >
                提取试题
              </button>
            </div>
          ) : (
            <div className="space-y-4 p-6">
              {questions.map((question, index) => (
                <div key={question.id || index} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex items-center space-x-3">
                      <span className="bg-blue-100 text-blue-800 text-sm font-medium px-2 py-1 rounded">
                        第{question.question_number}题
                      </span>
                      <span className="bg-green-100 text-green-800 text-sm font-medium px-2 py-1 rounded">
                        {question.question_type}
                      </span>
                      {question.score && (
                        <span className="bg-yellow-100 text-yellow-800 text-sm font-medium px-2 py-1 rounded">
                          {question.score}分
                        </span>
                      )}
                    </div>
                  </div>
                  
                  <div className="mb-3">
                    <h4 className="font-medium text-gray-900 mb-2">题目内容：</h4>
                    <div className="bg-gray-50 p-3 rounded text-gray-700 whitespace-pre-wrap">
                      {question.question_content}
                    </div>
                  </div>

                  {question.exam_points && (
                    <div className="mb-3">
                      <h4 className="font-medium text-gray-900 mb-2">相关考点：</h4>
                      <div className="bg-blue-50 p-3 rounded text-blue-700">
                        {question.exam_points}
                      </div>
                    </div>
                  )}

                  {question.answer_content && (
                    <div className="mb-3">
                      <h4 className="font-medium text-gray-900 mb-2">参考答案：</h4>
                      <div className="bg-green-50 p-3 rounded text-green-700">
                        {question.answer_content}
                      </div>
                    </div>
                  )}

                  {question.answer_explanation && (
                    <div className="mb-3">
                      <h4 className="font-medium text-gray-900 mb-2">答案解析：</h4>
                      <div className="bg-purple-50 p-3 rounded text-purple-700">
                        {question.answer_explanation}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );

  return (
    <div className="p-6">
      {currentView === 'papers' && renderPaperList()}
      {renderUploadModal()}
      {renderAddPaperModal()}
      {renderPreviewModal()}
      {currentView === 'questions' && renderQuestionsList()}
      {/* 这里可以继续实现试题列表、上传/编辑弹窗等 */}
    </div>
  );
};

export default ExamPaperManagement;
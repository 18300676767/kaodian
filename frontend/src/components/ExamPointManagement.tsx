import React, { useState, useEffect, useCallback } from 'react';
import { examPointAPI } from '../services/api';
import { ExamPoint, ExamPointQuery, PROVINCES, SUBJECTS, GRADES, SEMESTERS, EXCEL_COLUMNS, SAMPLE_EXAM_POINTS } from '../config/examPointConfig';
import { readExamPointsFromExcel, exportExamPointsToExcel, generateExcelTemplate, validateExcelFile } from '../utils/excelUtils';
import PaginationTool from './PaginationTool';
import ExamPointDetailModal from './ExamPointDetailModal';

interface ExamPointManagementProps {
  currentUser: any;
}

const ExamPointManagement: React.FC<ExamPointManagementProps> = ({ currentUser }) => {
  const [examPoints, setExamPoints] = useState<ExamPoint[]>([]);
  const [loading, setLoading] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showImportModal, setShowImportModal] = useState(false);
  const [currentExamPoint, setCurrentExamPoint] = useState<ExamPoint | null>(null);
  // 查询条件 state
  const [query, setQuery] = useState<{
    province_id?: number;
    subject?: string;
    grade?: string;
    semester?: string;
    level1_point?: string;
    level2_point?: string;
    level3_point?: string;
    description?: string;
  }>({});
  const [importData, setImportData] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [message, setMessage] = useState('');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [total, setTotal] = useState(0);
  const [showDetailModal, setShowDetailModal] = useState(false);
  // 1. 在组件顶部添加省份映射状态
  const [provinceList, setProvinceList] = useState<{id:number, name:string}[]>([]);

  // 2. useEffect中加载省份列表
  useEffect(() => {
    const loadProvinces = async () => {
      try {
        const res = await fetch('http://localhost:8000/provinces', {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        if (res && res.ok) {
          const data = await res.json();
          setProvinceList(data);
        }
      } catch (err) {
        setProvinceList([]);
      }
    };
    loadProvinces();
  }, []);

  // 用 useCallback 包裹 fetchExamPoints
  const fetchExamPoints = useCallback(async () => {
    setLoading(true);
    try {
      const params: any = {};
      if (query.province_id) params.province_id = query.province_id;
      if (query.subject) params.subject = query.subject;
      if (query.grade) params.grade = query.grade;
      if (query.semester) params.semester = query.semester;
      if (query.level1_point) params.level1_point = query.level1_point;
      if (query.level2_point) params.level2_point = query.level2_point;
      if (query.level3_point) params.level3_point = query.level3_point;
      if (query.description) params.description = query.description;

      const data = await examPointAPI.getExamPoints({ ...params, page, page_size: pageSize });
      if (Array.isArray(data)) {
        setExamPoints(data.slice((page - 1) * pageSize, page * pageSize));
        setTotal(data.length);
      } else if (data && typeof data === 'object') {
        setExamPoints((data as any).items || []);
        setTotal((data as any).total || 0);
      } else {
        setExamPoints([]);
        setTotal(0);
      }
      console.log('✅ 获取考点列表成功');
    } catch (error) {
      console.error('❌ 获取考点列表失败:', error);
      setMessage('获取考点列表失败');
    } finally {
      setLoading(false);
    }
  }, [query, page, pageSize]);

  useEffect(() => {
    fetchExamPoints();
  }, [fetchExamPoints]);

  const handleAdd = async (examPoint: ExamPoint) => {
    try {
      const newExamPoint = {
        ...examPoint,
        added_by: currentUser.username,
        added_date: new Date().toISOString().split('T')[0],
        is_active: true
      };
      await examPointAPI.createExamPoint(newExamPoint);
      setShowAddModal(false);
      fetchExamPoints();
      setMessage('✅ 考点添加成功');
      alert('🎉 考点添加成功！');
    } catch (error) {
      console.error('❌ 添加考点失败:', error);
      setMessage('添加考点失败');
    }
  };

  const handleEdit = async (examPoint: ExamPoint) => {
    try {
      await examPointAPI.updateExamPoint(examPoint.id!, examPoint);
      setShowEditModal(false);
      fetchExamPoints();
      setMessage('✅ 考点更新成功');
      alert('🎉 考点更新成功！');
    } catch (error) {
      console.error('❌ 更新考点失败:', error);
      setMessage('更新考点失败');
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('确定要删除这个考点吗？')) {
      try {
        await examPointAPI.deleteExamPoint(id);
        fetchExamPoints();
        setMessage('✅ 考点删除成功');
        alert('🗑️ 考点删除成功！');
      } catch (error) {
        console.error('❌ 删除考点失败:', error);
        setMessage('删除考点失败');
      }
    }
  };

  // 自动格式化描述，补全斜杠并包裹LaTeX公式
  function autoFormatDescription(desc: string): string {
    let fixed = desc.replace(/([^\\])frac/g, '$1\\frac')
      .replace(/([^\\])sqrt/g, '$1\\sqrt')
      .replace(/([^\\])leq/g, '$1\\leq')
      .replace(/([^\\])geq/g, '$1\\geq')
      .replace(/([^\\])sum/g, '$1\\sum')
      .replace(/([^\\])int/g, '$1\\int')
      .replace(/([^\\])log/g, '$1\\log')
      .replace(/([^\\])sin/g, '$1\\sin')
      .replace(/([^\\])cos/g, '$1\\cos')
      .replace(/([^\\])tan/g, '$1\\tan')
      .replace(/([^\\])cdot/g, '$1\\cdot')
      .replace(/([^\\])times/g, '$1\\times')
      .replace(/([^\\])div/g, '$1\\div')
      .replace(/([^\\])left/g, '$1\\left')
      .replace(/([^\\])right/g, '$1\\right');
    // 以行为单位处理
    return fixed.split(/\n|<br\s*\/?>/g).map(line => {
      const latexKeywords = /\\frac|\\sqrt|\\leq|\\geq|\\sum|\\int|\\log|\\sin|\\cos|\\tan|\^|_|\\cdot|\\times|\\div|\\left|\\right/;
      if (latexKeywords.test(line) && !line.trim().startsWith('$')) {
        return `$${line}$`;
      }
      return line;
    }).join('\n');
  }

  const handleImportJSON = async () => {
    try {
      const data = JSON.parse(importData);
      const examPoints = (Array.isArray(data) ? data : [data]).map(item => ({
        ...item,
        description: autoFormatDescription(item.description || '')
      }));
      await examPointAPI.importExamPoints(examPoints);
      setShowImportModal(false);
      setImportData('');
      fetchExamPoints();
      setMessage('✅ JSON导入成功');
      alert('📥 JSON数据导入成功！');
    } catch (error) {
      console.error('❌ JSON导入失败:', error);
      setMessage('JSON格式错误或导入失败');
    }
  };

  const handleImportExcel = async () => {
    if (!selectedFile) {
      setMessage('请选择Excel文件');
      return;
    }

    try {
      // 验证文件格式
      await validateExcelFile(selectedFile);
      
      // 读取Excel数据
      let examPoints = await readExamPointsFromExcel(selectedFile);
      
      // 批量导入到后端
      examPoints = examPoints.map(item => ({
        ...item,
        description: autoFormatDescription(item.description || '')
      }));
      await examPointAPI.importExamPoints(examPoints);
      
      setShowImportModal(false);
      setSelectedFile(null);
      fetchExamPoints();
      setMessage('✅ Excel导入成功');
      alert(`📥 Excel文件导入成功！共导入 ${examPoints.length} 条数据`);
    } catch (error) {
      console.error('❌ Excel导入失败:', error);
      setMessage(`Excel导入失败: ${error instanceof Error ? error.message : '未知错误'}`);
    }
  };

  const handleExport = async () => {
    try {
      // 使用前端Excel工具导出，传入 provinceList
      exportExamPointsToExcel(examPoints, provinceList, '考点数据');
      setMessage('✅ 导出成功');
      alert('📤 考点数据导出成功！');
    } catch (error) {
      console.error('❌ 导出失败:', error);
      setMessage('导出失败');
    }
  };

  const handleShowDetail = (examPoint: ExamPoint) => {
    setCurrentExamPoint(examPoint);
    setShowDetailModal(true);
  };
  const handleCloseDetail = () => {
    setShowDetailModal(false);
  };

  const renderQueryForm = () => (
    <div className="bg-white rounded-lg shadow p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">查询条件</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">省份</label>
          <select
            value={query.province_id || ''}
            onChange={e => setQuery({ ...query, province_id: e.target.value ? Number(e.target.value) : undefined })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">全部省份</option>
            {provinceList.map((province) => (
              <option key={province.id} value={province.id}>{province.name}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">科目</label>
          <select
            value={query.subject || ''}
            onChange={(e) => setQuery({ ...query, subject: e.target.value || undefined })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">全部科目</option>
            {SUBJECTS.map(subject => (
              <option key={subject} value={subject}>{subject}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">年级</label>
          <select
            value={query.grade || ''}
            onChange={(e) => setQuery({ ...query, grade: e.target.value || undefined })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">全部年级</option>
            {GRADES.map(grade => (
              <option key={grade} value={grade}>{grade}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">学期</label>
          <select
            value={query.semester || ''}
            onChange={(e) => setQuery({ ...query, semester: e.target.value || undefined })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">全部学期</option>
            {SEMESTERS.map(semester => (
              <option key={semester} value={semester}>{semester}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">一级考点</label>
          <input
            type="text"
            value={query.level1_point || ''}
            onChange={(e) => setQuery({ ...query, level1_point: e.target.value || undefined })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="输入一级考点"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">二级考点</label>
          <input
            type="text"
            value={query.level2_point || ''}
            onChange={(e) => setQuery({ ...query, level2_point: e.target.value || undefined })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="输入二级考点"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">三级考点</label>
          <input
            type="text"
            value={query.level3_point || ''}
            onChange={(e) => setQuery({ ...query, level3_point: e.target.value || undefined })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="输入三级考点"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">考点描述</label>
          <input
            type="text"
            value={query.description || ''}
            onChange={(e) => setQuery({ ...query, description: e.target.value || undefined })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="输入考点描述"
          />
        </div>
      </div>
      
      <div className="mt-4 flex space-x-2">
        <button
          onClick={() => setQuery({})}
          className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
        >
          清空条件
        </button>
        <button
          onClick={fetchExamPoints}
          className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
        >
          查询
        </button>
      </div>
    </div>
  );

  const renderExamPointTable = () => (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-semibold text-gray-900">考点列表</h3>
          <div className="flex space-x-2">
            <button
              onClick={() => setShowAddModal(true)}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              添加考点
            </button>
            <button
              onClick={() => setShowImportModal(true)}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              导入数据
            </button>
            <button
              onClick={handleExport}
              className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
            >
              导出数据
            </button>
          </div>
        </div>
      </div>
      
      {loading ? (
        <div className="p-6 text-center">
          <div className="animate-spin h-8 w-8 text-indigo-600 mx-auto"></div>
          <p className="mt-2 text-gray-600">加载中...</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">省份</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">科目</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">年级</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">学期</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">一级考点</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">二级考点</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">三级考点</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">覆盖率</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {examPoints.map((examPoint) => (
                <tr key={examPoint.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{provinceList.find(p => p.id === examPoint.province_id)?.name || ''}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{examPoint.subject}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{examPoint.grade}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{examPoint.semester}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{examPoint.level1_point}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{examPoint.level2_point}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{examPoint.level3_point}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{examPoint.coverage_rate}%</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      examPoint.is_active 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {examPoint.is_active ? '有效' : '无效'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button
                      onClick={() => {
                        setCurrentExamPoint(examPoint);
                        setShowEditModal(true);
                      }}
                      className="text-indigo-600 hover:text-indigo-900 mr-3"
                    >
                      编辑
                    </button>
                    <button
                      onClick={() => handleShowDetail(examPoint)}
                      className="text-blue-600 hover:text-blue-900 mr-3"
                    >
                      详情
                    </button>
                    <button
                      onClick={() => handleDelete(examPoint.id!)}
                      className="text-red-600 hover:text-red-900"
                    >
                      删除
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {showDetailModal && (
        <ExamPointDetailModal examPoint={currentExamPoint} onClose={handleCloseDetail} provinceList={provinceList} />
      )}
    </div>
  );

  return (
    <div className="p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">考点管理</h1>
        
        {message && (
          <div className={`mb-4 p-4 rounded-md ${
            message.includes('成功') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
          }`}>
            {message}
          </div>
        )}
        
        {renderQueryForm()}
        {renderExamPointTable()}
        <div style={{ margin: '16px 0' }}>
          <PaginationTool
            total={total}
            page={page}
            pageSize={pageSize}
            onPageChange={setPage}
            onPageSizeChange={(size) => { setPageSize(size); setPage(1); }}
          />
        </div>
        
        {/* 添加考点模态框 */}
        {showAddModal && (
          <ExamPointModal
            examPoint={null}
            onSave={handleAdd}
            onCancel={() => setShowAddModal(false)}
            title="添加考点"
            provinceList={provinceList}
          />
        )}
        
        {/* 编辑考点模态框 */}
        {showEditModal && currentExamPoint && (
          <ExamPointModal
            examPoint={currentExamPoint}
            onSave={handleEdit}
            onCancel={() => setShowEditModal(false)}
            title="编辑考点"
            provinceList={provinceList}
          />
        )}
        
        {/* 导入数据模态框 */}
        {showImportModal && (
          <ImportModal
            onImportJSON={handleImportJSON}
            onImportExcel={handleImportExcel}
            onCancel={() => setShowImportModal(false)}
            importData={importData}
            setImportData={setImportData}
            selectedFile={selectedFile}
            setSelectedFile={setSelectedFile}
          />
        )}
      </div>
    </div>
  );
};

// 考点表单模态框组件
interface ExamPointModalProps {
  examPoint: ExamPoint | null;
  onSave: (examPoint: ExamPoint) => void;
  onCancel: () => void;
  title: string;
  provinceList: {id:number, name:string}[];
}

const ExamPointModal: React.FC<ExamPointModalProps> = ({ examPoint, onSave, onCancel, title, provinceList }) => {
  const [formData, setFormData] = useState<ExamPoint>({
    province_id: examPoint?.province_id || undefined,
    subject: examPoint?.subject || '',
    grade: examPoint?.grade || '',
    semester: examPoint?.semester || '',
    level1_point: examPoint?.level1_point || '',
    level2_point: examPoint?.level2_point || '',
    level3_point: examPoint?.level3_point || '',
    description: examPoint?.description || '',
    coverage_rate: examPoint?.coverage_rate || 0,
    added_by: examPoint?.added_by || '',
    added_date: examPoint?.added_date || '',
    is_active: examPoint?.is_active ?? true,
    id: examPoint?.id,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave({ ...formData, province_id: formData.province_id });
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
        <div className="mt-3">
          <h3 className="text-lg font-medium text-gray-900 mb-4">{title}</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">省份 *</label>
                <select
                  required
                  value={formData.province_id || ''}
                  onChange={e => {
                    const pid = Number(e.target.value);
                    setFormData({ ...formData, province_id: pid });
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="">选择省份</option>
                  {provinceList.map((p: {id:number, name:string}) => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">科目 *</label>
                <select
                  required
                  value={formData.subject}
                  onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="">选择科目</option>
                  {SUBJECTS.map(subject => (
                    <option key={subject} value={subject}>{subject}</option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">年级 *</label>
                <select
                  required
                  value={formData.grade}
                  onChange={(e) => setFormData({ ...formData, grade: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="">选择年级</option>
                  {GRADES.map(grade => (
                    <option key={grade} value={grade}>{grade}</option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">学期 *</label>
                <select
                  required
                  value={formData.semester}
                  onChange={(e) => setFormData({ ...formData, semester: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="">选择学期</option>
                  {SEMESTERS.map(semester => (
                    <option key={semester} value={semester}>{semester}</option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">一级考点 *</label>
                <input
                  type="text"
                  required
                  value={formData.level1_point}
                  onChange={(e) => setFormData({ ...formData, level1_point: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="输入一级考点"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">二级考点</label>
                <input
                  type="text"
                  value={formData.level2_point}
                  onChange={(e) => setFormData({ ...formData, level2_point: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="输入二级考点"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">三级考点</label>
                <input
                  type="text"
                  value={formData.level3_point}
                  onChange={(e) => setFormData({ ...formData, level3_point: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="输入三级考点"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">覆盖率 (%) *</label>
                <input
                  type="number"
                  required
                  min="0"
                  max="100"
                  value={formData.coverage_rate}
                  onChange={e => setFormData({ ...formData, coverage_rate: Number(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="输入覆盖率(0-100)"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">考点描述 *</label>
              <textarea
                required
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="输入考点描述"
              />
            </div>
            
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={formData.is_active}
                onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label className="ml-2 block text-sm text-gray-900">有效状态</label>
            </div>
            
            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={onCancel}
                className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
              >
                取消
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
              >
                保存
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

// 导入数据模态框组件
interface ImportModalProps {
  onImportJSON: () => void;
  onImportExcel: () => void;
  onCancel: () => void;
  importData: string;
  setImportData: (data: string) => void;
  selectedFile: File | null;
  setSelectedFile: (file: File | null) => void;
}

const ImportModal: React.FC<ImportModalProps> = ({
  onImportJSON,
  onImportExcel,
  onCancel,
  importData,
  setImportData,
  selectedFile,
  setSelectedFile
}) => {
  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
        <div className="mt-3">
          <h3 className="text-lg font-medium text-gray-900 mb-4">导入考点数据</h3>
          
          <div className="space-y-6">
            {/* JSON导入 */}
            <div>
              <h4 className="text-md font-medium text-gray-900 mb-2">JSON格式导入</h4>
              <textarea
                value={importData}
                onChange={(e) => setImportData(e.target.value)}
                rows={8}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="请输入JSON格式的考点数据..."
              />
              <div className="mt-2">
                <button
                  onClick={onImportJSON}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  导入JSON
                </button>
              </div>
            </div>
            
            {/* Excel导入 */}
            <div>
              <h4 className="text-md font-medium text-gray-900 mb-2">Excel文件导入</h4>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
                <input
                  type="file"
                  accept=".xlsx,.xls"
                  onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                  className="w-full"
                />
                <p className="mt-2 text-sm text-gray-500">
                  支持的格式：.xlsx, .xls
                </p>
                <p className="text-sm text-gray-500">
                  Excel列格式：{EXCEL_COLUMNS.map(col => col.label).join(', ')}
                </p>
              </div>
              <div className="mt-2">
                <button
                  onClick={onImportExcel}
                  disabled={!selectedFile}
                  className={`px-4 py-2 rounded-md ${
                    selectedFile 
                      ? 'bg-green-600 text-white hover:bg-green-700' 
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  导入Excel
                </button>
              </div>
            </div>
            
            {/* 示例数据 */}
            <div>
              <h4 className="text-md font-medium text-gray-900 mb-2">示例数据</h4>
              <div className="space-x-2">
                <button
                  onClick={() => setImportData(JSON.stringify(SAMPLE_EXAM_POINTS, null, 2))}
                  className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
                >
                  加载JSON示例
                </button>
                <button
                  onClick={generateExcelTemplate}
                  className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
                >
                  下载Excel模板
                </button>
              </div>
            </div>
          </div>
          
          <div className="mt-6 flex justify-end">
            <button
              onClick={onCancel}
              className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
            >
              关闭
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExamPointManagement; 
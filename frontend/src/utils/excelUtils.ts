import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';
import { ExamPoint, EXCEL_COLUMNS } from '../config/examPointConfig';

// 从Excel文件读取考点数据
export const readExamPointsFromExcel = (file: File): Promise<ExamPoint[]> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target?.result as ArrayBuffer);
        const workbook = XLSX.read(data, { type: 'array' });
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        const jsonData = XLSX.utils.sheet_to_json(worksheet);
        
        // 转换数据格式
        const examPoints: ExamPoint[] = jsonData.map((row: any, index: number) => {
          // 验证必需字段
          const requiredFields = EXCEL_COLUMNS.filter(col => col.required).map(col => col.key);
          for (const field of requiredFields) {
            if (!row[field]) {
              throw new Error(`第${index + 1}行缺少必需字段: ${field}`);
            }
          }
          
                     return {
             province: row.province || '',
             subject: row.subject || '',
             grade: row.grade || '',
             semester: row.semester || '',
             level1_point: row.level1_point || '',
             level2_point: row.level2_point || '',
             level3_point: row.level3_point || '',
             description: row.description || '',
             coverage_rate: parseFloat(row.coverage_rate) || 0,
             added_by: row.added_by || '',
             added_date: row.added_date || new Date().toISOString().split('T')[0],
             is_active: row.is_active === '是' || row.is_active === true || row.is_active === 1
           };
        });
        
        resolve(examPoints);
      } catch (error) {
        reject(error);
      }
    };
    
    reader.onerror = () => {
      reject(new Error('文件读取失败'));
    };
    
    reader.readAsArrayBuffer(file);
  });
};

// 导出考点数据到Excel文件
export const exportExamPointsToExcel = (examPoints: ExamPoint[], provinceList: {id:number, name:string}[], filename: string = '考点数据') => {
  // 准备导出数据
  const exportData = examPoints.map(point => ({
    '省份': provinceList.find(p => p.id === point.province_id)?.name || '',
    '科目': point.subject,
    '年级': point.grade,
    '学期': point.semester,
    '一级考点': point.level1_point,
    '二级考点': point.level2_point,
    '三级考点': point.level3_point,
    '考点描述': point.description,
    '历年高考覆盖率': point.coverage_rate,
    '添加人': point.added_by,
    '添加日期': point.added_date,
    '有效状态': point.is_active ? '是' : '否'
  }));
  
  // 创建工作簿
  const workbook = XLSX.utils.book_new();
  const worksheet = XLSX.utils.json_to_sheet(exportData);
  
  // 设置列宽
  const colWidths = [
    { wch: 10 }, // 省份
    { wch: 8 },  // 科目
    { wch: 8 },  // 年级
    { wch: 8 },  // 学期
    { wch: 15 }, // 一级考点
    { wch: 15 }, // 二级考点
    { wch: 15 }, // 三级考点
    { wch: 30 }, // 考点描述
    { wch: 12 }, // 历年高考覆盖率
    { wch: 10 }, // 添加人
    { wch: 12 }, // 添加日期
    { wch: 8 }   // 有效状态
  ];
  worksheet['!cols'] = colWidths;
  
  // 添加工作表到工作簿
  XLSX.utils.book_append_sheet(workbook, worksheet, '考点数据');
  
  // 生成Excel文件
  const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
  const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
  
  // 下载文件
  saveAs(blob, `${filename}_${new Date().toISOString().split('T')[0]}.xlsx`);
};

// 生成Excel模板
export const generateExcelTemplate = () => {
  // 创建示例数据
  const templateData = [
    {
      '省份': '北京',
      '科目': '数学',
      '年级': '高三',
      '学期': '上学期',
      '一级考点': '函数',
      '二级考点': '基本初等函数',
      '三级考点': '指数函数',
      '考点描述': '指数函数的基本性质和应用',
      '历年高考覆盖率': 85.5,
      '添加人': 'admin',
      '添加日期': '2024-01-15',
      '有效状态': '是'
    }
  ];
  
  // 创建工作簿
  const workbook = XLSX.utils.book_new();
  const worksheet = XLSX.utils.json_to_sheet(templateData);
  
  // 设置列宽
  const colWidths = [
    { wch: 10 }, // 省份
    { wch: 8 },  // 科目
    { wch: 8 },  // 年级
    { wch: 8 },  // 学期
    { wch: 15 }, // 一级考点
    { wch: 15 }, // 二级考点
    { wch: 15 }, // 三级考点
    { wch: 30 }, // 考点描述
    { wch: 12 }, // 历年高考覆盖率
    { wch: 10 }, // 添加人
    { wch: 12 }, // 添加日期
    { wch: 8 }   // 有效状态
  ];
  worksheet['!cols'] = colWidths;
  
  // 添加工作表到工作簿
  XLSX.utils.book_append_sheet(workbook, worksheet, '考点数据模板');
  
  // 生成Excel文件
  const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
  const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
  
  // 下载文件
  saveAs(blob, '考点数据导入模板.xlsx');
};

// 验证Excel文件格式
export const validateExcelFile = (file: File): Promise<boolean> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target?.result as ArrayBuffer);
        const workbook = XLSX.read(data, { type: 'array' });
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        const jsonData = XLSX.utils.sheet_to_json(worksheet);
        
        if (jsonData.length === 0) {
          reject(new Error('Excel文件为空'));
          return;
        }
        
        // 检查第一行是否包含必需的列
        const firstRow = jsonData[0] as any;
        const requiredColumns = EXCEL_COLUMNS.filter(col => col.required).map(col => col.key);
        
        for (const column of requiredColumns) {
          if (!(column in firstRow)) {
            reject(new Error(`缺少必需列: ${column}`));
            return;
          }
        }
        
        resolve(true);
      } catch (error) {
        reject(error);
      }
    };
    
    reader.onerror = () => {
      reject(new Error('文件读取失败'));
    };
    
    reader.readAsArrayBuffer(file);
  });
}; 
// 考点管理配置文件

// 考点数据结构定义
export interface ExamPoint {
  id?: number;
  province?: string;           // 省份（仅展示用，可选）
  province_id?: number;       // 省份ID（后端用）
  subject: string;            // 科目
  grade: string;              // 年级
  semester: string;           // 学期
  level1_point: string;       // 一级考点
  level2_point: string;       // 二级考点
  level3_point: string;       // 三级考点
  description: string;        // 考点描述
  coverage_rate: number;      // 历年高考覆盖率
  added_by: string;          // 添加人
  added_date: string;        // 添加日期
  is_active: boolean;         // 有效状态
}

// Excel导入格式定义
export const EXCEL_COLUMNS = [
  { key: 'province', label: '省份', required: true },
  { key: 'subject', label: '科目', required: true },
  { key: 'grade', label: '年级', required: true },
  { key: 'semester', label: '学期', required: true },
  { key: 'level1_point', label: '一级考点', required: true },
  { key: 'level2_point', label: '二级考点', required: false },
  { key: 'level3_point', label: '三级考点', required: false },
  { key: 'description', label: '考点描述', required: true },
  { key: 'coverage_rate', label: '历年高考覆盖率', required: true },
  { key: 'is_active', label: '有效状态', required: true }
];

// 查询条件接口
export interface ExamPointQuery {
  province?: string;
  subject?: string;
  grade?: string;
  semester?: string;
  level1_point?: string;
  level2_point?: string;
  level3_point?: string;
  description?: string;
  page?: number;
  page_size?: number;
}

// 省份选项
export const PROVINCES = [
  '北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江',
  '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南',
  '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州',
  '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆'
];

// 科目选项
export const SUBJECTS = [
  '语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理'
];

// 年级选项
export const GRADES = [
  '高一', '高二', '高三'
];

// 学期选项
export const SEMESTERS = [
  '上学期', '下学期'
];

// 默认考点数据示例
export const SAMPLE_EXAM_POINTS: ExamPoint[] = [
  {
    province: '北京',
    subject: '数学',
    grade: '高三',
    semester: '上学期',
    level1_point: '函数',
    level2_point: '基本初等函数',
    level3_point: '指数函数',
    description: '指数函数的基本性质和应用',
    coverage_rate: 85.5,
    added_by: 'admin',
    added_date: '2024-01-15',
    is_active: true
  },
  {
    province: '上海',
    subject: '语文',
    grade: '高三',
    semester: '下学期',
    level1_point: '现代文阅读',
    level2_point: '文学类文本',
    level3_point: '小说阅读',
    description: '小说文本的阅读理解和分析',
    coverage_rate: 92.3,
    added_by: 'admin',
    added_date: '2024-01-16',
    is_active: true
  }
]; 
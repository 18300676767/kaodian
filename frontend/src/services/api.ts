import axios from 'axios';
import { ExamPoint, ExamPointQuery } from '../config/examPointConfig';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器 - 添加token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface LoginData {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  phone?: string;
  real_name?: string;
  age?: number;
  grade?: string;
  province_id?: number;
  city_id?: number;
}

export interface Province {
  id: number;
  name: string;
  code: string;
  created_at: string;
  updated_at: string;
}

export interface City {
  id: number;
  name: string;
  code: string;
  province_id: number;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  phone?: string;
  real_name?: string;
  age?: number;
  grade?: string;
  province_id?: number;
  city_id?: number;
  is_active: boolean;
  is_approved: boolean;
  is_deleted: boolean;
  created_at: string;
  updated_at?: string;
  approved_at?: string;
  deleted_at?: string;
  province?: Province;
  city?: City;
}

export interface UserList {
  id: number;
  username: string;
  email: string;
  phone?: string;
  real_name?: string;
  age?: number;
  grade?: string;
  province_id?: number;
  city_id?: number;
  is_active: boolean;
  is_approved: boolean;
  is_deleted: boolean;
  created_at: string;
  updated_at?: string;
  approved_at?: string;
  deleted_at?: string;
  province?: Province;
  city?: City;
}

export interface UserUpdateData {
  username?: string;
  email?: string;
  phone?: string;
  real_name?: string;
  age?: number;
  grade?: string;
  province_id?: number;
  city_id?: number;
  password?: string;
}

export interface ApproveUserData {
  is_approved: boolean;
}

export interface ToggleUserStatusResponse {
  message: string;
}

// 省份和城市相关API
export const locationAPI = {
  // 获取所有省份
  getProvinces: async (): Promise<Province[]> => {
    const response = await api.get('/provinces');
    return response.data;
  },

  // 根据省份ID获取城市列表
  getCitiesByProvince: async (provinceId: number): Promise<City[]> => {
    const response = await api.get(`/provinces/${provinceId}/cities`);
    return response.data;
  },
};

// 认证相关API
export const authAPI = {
  // 用户登录
  login: async (data: LoginData) => {
    const formData = new FormData();
    formData.append('username', data.username);
    formData.append('password', data.password);
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    
    return response.data;
  },

  // 用户注册
  register: async (data: RegisterData) => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  // 获取当前用户信息
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/users/me');
    return response.data;
  },
};

// 用户管理相关API
export const userAPI = {
  // 获取用户列表
  getUsers: async (): Promise<UserList[]> => {
    const response = await api.get('/users/');
    return response.data;
  },

  // 获取单个用户信息
  getUser: async (userId: number): Promise<User> => {
    const response = await api.get(`/users/${userId}`);
    return response.data;
  },

  // 更新用户信息
  updateUser: async (userId: number, data: UserUpdateData): Promise<User> => {
    const response = await api.put(`/users/${userId}`, data);
    return response.data;
  },

  // 审核用户
  approveUser: async (userId: number, data: ApproveUserData): Promise<User> => {
    const response = await api.put(`/users/${userId}/approve`, data);
    return response.data;
  },

  // 切换用户状态（激活/禁用）
  toggleUserStatus: async (userId: number): Promise<ToggleUserStatusResponse> => {
    const response = await api.put(`/users/${userId}/toggle-status`);
    return response.data;
  },

  // 删除用户（软删除）
  deleteUser: async (userId: number): Promise<{ message: string }> => {
    const response = await api.delete(`/users/${userId}`);
    return response.data;
  },
};

export const healthAPI = {
  check: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

// 考点管理相关API
export const examPointAPI = {
  // 获取考点列表
  getExamPoints: async (query?: ExamPointQuery): Promise<ExamPoint[]> => {
    const params = new URLSearchParams();
    if (query) {
      Object.entries(query).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });
    }
    const response = await api.get(`/exam-points?${params.toString()}`);
    return response.data;
  },

  // 获取单个考点信息
  getExamPoint: async (id: number): Promise<ExamPoint> => {
    const response = await api.get(`/exam-points/${id}`);
    return response.data;
  },

  // 创建考点
  createExamPoint: async (data: ExamPoint): Promise<ExamPoint> => {
    const response = await api.post('/exam-points', data);
    return response.data;
  },

  // 更新考点
  updateExamPoint: async (id: number, data: Partial<ExamPoint>): Promise<ExamPoint> => {
    const response = await api.put(`/exam-points/${id}`, data);
    return response.data;
  },

  // 删除考点
  deleteExamPoint: async (id: number): Promise<{ message: string }> => {
    const response = await api.delete(`/exam-points/${id}`);
    return response.data;
  },

  // 批量导入考点（JSON格式）
  importExamPoints: async (data: ExamPoint[]): Promise<{ message: string; imported_count: number }> => {
    const response = await api.post('/exam-points/import', { exam_points: data });
    return response.data;
  },

  // 上传Excel文件导入考点
  uploadExcelFile: async (file: File): Promise<{ message: string; imported_count: number }> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/exam-points/upload-excel', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // 导出考点数据
  exportExamPoints: async (query?: ExamPointQuery): Promise<Blob> => {
    const params = new URLSearchParams();
    if (query) {
      Object.entries(query).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });
    }
    const response = await api.get(`/exam-points/export?${params.toString()}`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

export default api; 
import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import ExamPointManagement from '../ExamPointManagement';

// Mock API服务
jest.mock('../../services/api', () => ({
  examPointAPI: {
    getExamPoints: jest.fn().mockResolvedValue([
      { id: 1, level1_point: '函数', level2_point: '基本初等函数', level3_point: '指数函数', description: '指数函数性质', coverage_rate: 30, status: '正常' }
    ]),
    deleteExamPoint: jest.fn().mockResolvedValue({ message: '删除成功' })
  }
}));

const mockUser = {
  id: 1,
  username: 'testuser',
  real_name: '测试用户',
  email: 'test@example.com',
  phone: '13800138000',
  age: 18,
  grade: '高三',
  province_id: 1,
  city_id: 1,
  is_active: true,
  is_approved: true,
  is_deleted: false,
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
  approved_at: '2024-01-01T00:00:00Z',
  deleted_at: undefined,
  province: { id: 1, name: '北京', code: 'BJ', created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z' },
  city: { id: 1, name: '北京市', code: 'BJS', created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z', province_id: 1 }
};

describe('ExamPointManagement', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders exam point management interface', async () => {
    await act(async () => {
      render(<ExamPointManagement currentUser={mockUser} />);
    });
    
    // 验证主要界面元素
    expect(screen.getByText('考点管理')).toBeInTheDocument();
    expect(screen.getByText('查询条件')).toBeInTheDocument();
    expect(screen.getByText('考点列表')).toBeInTheDocument();
  });

  test('renders search form fields', async () => {
    await act(async () => {
      render(<ExamPointManagement currentUser={mockUser} />);
    });
    
    // 验证搜索表单字段
    expect(screen.getAllByText('省份')[0]).toBeInTheDocument();
    expect(screen.getAllByText('科目')[0]).toBeInTheDocument();
    expect(screen.getAllByText('年级')[0]).toBeInTheDocument();
    expect(screen.getAllByText('学期')[0]).toBeInTheDocument();
    expect(screen.getAllByText('一级考点')[0]).toBeInTheDocument();
    expect(screen.getAllByText('二级考点')[0]).toBeInTheDocument();
    expect(screen.getAllByText('三级考点')[0]).toBeInTheDocument();
    expect(screen.getAllByText('考点描述')[0]).toBeInTheDocument();
  });

  test('renders action buttons', async () => {
    await act(async () => {
      render(<ExamPointManagement currentUser={mockUser} />);
    });
    
    // 验证操作按钮
    expect(screen.getByText('添加考点')).toBeInTheDocument();
    expect(screen.getByText('导入数据')).toBeInTheDocument();
    expect(screen.getByText('导出数据')).toBeInTheDocument();
    expect(screen.getByText('查询')).toBeInTheDocument();
    expect(screen.getByText('清空条件')).toBeInTheDocument();
  });

  test('renders table headers', async () => {
    await act(async () => {
      render(<ExamPointManagement currentUser={mockUser} />);
    });
    await waitFor(() => {
      expect(screen.getByText('覆盖率')).toBeInTheDocument();
      expect(screen.getByText('状态')).toBeInTheDocument();
      expect(screen.getByText('操作')).toBeInTheDocument();
    });
  });
}); 
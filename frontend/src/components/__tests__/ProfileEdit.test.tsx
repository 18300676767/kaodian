import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ProfileEdit from '../ProfileEdit';

// Mock API服务
jest.mock('../../services/api', () => ({
  locationAPI: {
    getProvinces: jest.fn().mockResolvedValue([
      { id: 1, name: '北京', code: 'BJ', created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z' }
    ]),
    getCitiesByProvince: jest.fn().mockResolvedValue([
      { id: 1, name: '北京市', code: 'BJS', created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z', province_id: 1 }
    ])
  },
  userAPI: {
    updateUser: jest.fn().mockResolvedValue({})
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

describe('ProfileEdit', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders profile edit form', async () => {
    render(<ProfileEdit currentUser={mockUser} onUpdate={() => {}} />);
    
    // 等待异步加载完成
    await waitFor(() => {
      expect(screen.getByDisplayValue('test@example.com')).toBeInTheDocument();
    });
    
    // 验证表单元素
    expect(screen.getByDisplayValue('test@example.com')).toBeInTheDocument();
    expect(screen.getByDisplayValue('13800138000')).toBeInTheDocument();
    expect(screen.getByDisplayValue('18')).toBeInTheDocument();
    expect(screen.getByDisplayValue('高三')).toBeInTheDocument();
  });

  test('renders and updates profile', async () => {
    render(<ProfileEdit currentUser={mockUser} onUpdate={() => {}} />);
    
    // 等待异步加载完成
    await waitFor(() => {
      expect(screen.getByDisplayValue('test@example.com')).toBeInTheDocument();
    });
    
    // 修改表单数据
    const realNameInput = screen.getByDisplayValue('测试用户');
    fireEvent.change(realNameInput, { target: { value: '新名字' } });
    
    // 提交表单
    fireEvent.click(screen.getByText('保存更改'));
    
    // 验证API调用
    await waitFor(() => {
      const { userAPI } = require('../../services/api');
      expect(userAPI.updateUser).toHaveBeenCalled();
    });
  });

  test('renders form fields correctly', async () => {
    render(<ProfileEdit currentUser={mockUser} onUpdate={() => {}} />);
    
    // 等待异步加载完成
    await waitFor(() => {
      expect(screen.getByDisplayValue('test@example.com')).toBeInTheDocument();
    });
    
    // 验证所有表单字段
    expect(screen.getByLabelText('真实姓名')).toBeInTheDocument();
    expect(screen.getByLabelText('邮箱')).toBeInTheDocument();
    expect(screen.getByLabelText('手机号')).toBeInTheDocument();
    expect(screen.getByLabelText('年龄')).toBeInTheDocument();
    expect(screen.getByLabelText('年级')).toBeInTheDocument();
    expect(screen.getByLabelText('省份')).toBeInTheDocument();
    expect(screen.getByLabelText('城市')).toBeInTheDocument();
  });
}); 
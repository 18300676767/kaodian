import React, { useState, useEffect } from 'react';
import { userAPI, locationAPI, UserList, User, Province, City } from '../services/api';

interface UserManagementProps {
  currentUser: User;
}

const UserManagement: React.FC<UserManagementProps> = ({ currentUser }) => {
  const [users, setUsers] = useState<UserList[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedUser, setSelectedUser] = useState<UserList | null>(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editForm, setEditForm] = useState({
    username: '',
    email: '',
    phone: '',
    real_name: '',
    age: '',
    grade: '',
    province_id: '',
    city_id: '',
    password: ''
  });
  const [provinces, setProvinces] = useState<Province[]>([]);
  const [cities, setCities] = useState<City[]>([]);
  const [loadingProvinces, setLoadingProvinces] = useState(true);
  const [loadingCities, setLoadingCities] = useState(false);

  useEffect(() => {
    loadUsers();
    loadProvinces();
  }, []);

  useEffect(() => {
    if (editForm.province_id) {
      loadCities(parseInt(editForm.province_id));
    } else {
      setCities([]);
      setEditForm(prev => ({ ...prev, city_id: '' }));
    }
  }, [editForm.province_id]);

  const loadProvinces = async () => {
    try {
      setLoadingProvinces(true);
      const provincesData = await locationAPI.getProvinces();
      setProvinces(provincesData);
    } catch (err) {
      console.error('❌ 加载省份数据失败:', err);
      setError('加载省份数据失败');
    } finally {
      setLoadingProvinces(false);
    }
  };

  const loadCities = async (provinceId: number) => {
    try {
      setLoadingCities(true);
      const citiesData = await locationAPI.getCitiesByProvince(provinceId);
      setCities(citiesData);
    } catch (err) {
      console.error('❌ 加载城市数据失败:', err);
      setError('加载城市数据失败');
    } finally {
      setLoadingCities(false);
    }
  };

  const loadUsers = async () => {
    try {
      setLoading(true);
      const userList = await userAPI.getUsers();
      setUsers(userList);
      setError(null);
    } catch (err) {
      setError('加载用户列表失败');
      console.error('❌ 加载用户列表失败:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleApproveUser = async (userId: number, approved: boolean) => {
    try {
      await userAPI.approveUser(userId, { is_approved: approved });
      console.log(`✅ 用户${approved ? '审核通过' : '取消审核'}成功`);
      loadUsers(); // 重新加载用户列表
    } catch (err) {
      console.error('❌ 审核用户失败:', err);
      setError('审核用户失败');
    }
  };

  const handleToggleUserStatus = async (userId: number) => {
    try {
      const result = await userAPI.toggleUserStatus(userId);
      console.log(`✅ ${result.message}`);
      loadUsers(); // 重新加载用户列表
    } catch (err) {
      console.error('❌ 切换用户状态失败:', err);
      setError('切换用户状态失败');
    }
  };

  const handleDeleteUser = async (userId: number) => {
    if (!window.confirm('确定要删除这个用户吗？')) {
      return;
    }

    try {
      await userAPI.deleteUser(userId);
      console.log('✅ 用户删除成功');
      loadUsers(); // 重新加载用户列表
    } catch (err) {
      console.error('❌ 删除用户失败:', err);
      setError('删除用户失败');
    }
  };

  const handleEditUser = (user: UserList) => {
    setSelectedUser(user);
    setEditForm({
      username: user.username || '',
      email: user.email || '',
      phone: user.phone || '',
      real_name: user.real_name || '',
      age: user.age?.toString() || '',
      grade: user.grade || '',
      province_id: user.province_id?.toString() || '',
      city_id: user.city_id?.toString() || '',
      password: ''
    });
    setShowEditModal(true);
  };

  const handleUpdateUser = async () => {
    if (!selectedUser) return;

    try {
      const updateData: any = { ...editForm };
      
      // 移除空值
      Object.keys(updateData).forEach(key => {
        if (updateData[key] === '') {
          delete updateData[key];
        }
      });

      // 转换数字字段
      if (updateData.age) {
        updateData.age = parseInt(updateData.age);
      }
      if (updateData.province_id) {
        updateData.province_id = parseInt(updateData.province_id);
      }
      if (updateData.city_id) {
        updateData.city_id = parseInt(updateData.city_id);
      }

      await userAPI.updateUser(selectedUser.id, updateData);
      console.log('✅ 用户信息更新成功');
      setShowEditModal(false);
      loadUsers(); // 重新加载用户列表
    } catch (err) {
      console.error('❌ 更新用户信息失败:', err);
      setError('更新用户信息失败');
    }
  };

  if (loading) {
    return (
      <div className="flex-1 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">加载中...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="bg-white shadow-lg rounded-lg overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-2xl font-bold text-gray-900">用户管理</h2>
            <p className="mt-1 text-sm text-gray-600">管理系统中的所有用户</p>
          </div>

          {error && (
            <div className="bg-red-50 border-l-4 border-red-400 p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              </div>
            </div>
          )}

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    用户信息
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    地区
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    状态
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    注册时间
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    操作
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {users.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <div className="h-10 w-10 rounded-full bg-blue-500 flex items-center justify-center">
                            <span className="text-white font-medium">
                              {user.username.charAt(0).toUpperCase()}
                            </span>
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">
                            {user.username}
                          </div>
                          <div className="text-sm text-gray-500">
                            {user.email}
                          </div>
                          {user.real_name && (
                            <div className="text-sm text-gray-500">
                              姓名: {user.real_name}
                            </div>
                          )}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {user.province?.name && user.city?.name ? (
                          <span>{user.province.name} {user.city.name}</span>
                        ) : (
                          <span className="text-gray-400">未设置</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex flex-col space-y-1">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          user.is_active 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {user.is_active ? '激活' : '禁用'}
                        </span>
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          user.is_approved 
                            ? 'bg-blue-100 text-blue-800' 
                            : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {user.is_approved ? '已审核' : '待审核'}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(user.created_at).toLocaleDateString('zh-CN')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleEditUser(user)}
                          className="text-indigo-600 hover:text-indigo-900"
                        >
                          编辑
                        </button>
                        <button
                          onClick={() => handleApproveUser(user.id, !user.is_approved)}
                          className={`${
                            user.is_approved 
                              ? 'text-yellow-600 hover:text-yellow-900' 
                              : 'text-green-600 hover:text-green-900'
                          }`}
                        >
                          {user.is_approved ? '取消审核' : '审核通过'}
                        </button>
                        <button
                          onClick={() => handleToggleUserStatus(user.id)}
                          className={`${
                            user.is_active 
                              ? 'text-orange-600 hover:text-orange-900' 
                              : 'text-green-600 hover:text-green-900'
                          }`}
                        >
                          {user.is_active ? '禁用' : '激活'}
                        </button>
                        <button
                          onClick={() => handleDeleteUser(user.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          删除
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* 编辑用户模态框 */}
        {showEditModal && selectedUser && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 mb-4">编辑用户信息</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">用户名</label>
                    <input
                      type="text"
                      value={editForm.username}
                      onChange={(e) => setEditForm({...editForm, username: e.target.value})}
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">邮箱</label>
                    <input
                      type="email"
                      value={editForm.email}
                      onChange={(e) => setEditForm({...editForm, email: e.target.value})}
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">手机号</label>
                    <input
                      type="text"
                      value={editForm.phone}
                      onChange={(e) => setEditForm({...editForm, phone: e.target.value})}
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">真实姓名</label>
                    <input
                      type="text"
                      value={editForm.real_name}
                      onChange={(e) => setEditForm({...editForm, real_name: e.target.value})}
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">年龄</label>
                    <input
                      type="number"
                      value={editForm.age}
                      onChange={(e) => setEditForm({...editForm, age: e.target.value})}
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">年级</label>
                    <input
                      type="text"
                      value={editForm.grade}
                      onChange={(e) => setEditForm({...editForm, grade: e.target.value})}
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">省份</label>
                    <select
                      value={editForm.province_id}
                      onChange={(e) => setEditForm({...editForm, province_id: e.target.value})}
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                      disabled={loadingProvinces}
                    >
                      <option value="">请选择省份</option>
                      {provinces.map((province) => (
                        <option key={province.id} value={province.id}>
                          {province.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">城市</label>
                    <select
                      value={editForm.city_id}
                      onChange={(e) => setEditForm({...editForm, city_id: e.target.value})}
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                      disabled={!editForm.province_id || loadingCities}
                    >
                      <option value="">请选择城市</option>
                      {cities.map((city) => (
                        <option key={city.id} value={city.id}>
                          {city.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">新密码（可选）</label>
                    <input
                      type="password"
                      value={editForm.password}
                      onChange={(e) => setEditForm({...editForm, password: e.target.value})}
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                    />
                  </div>
                </div>
                <div className="flex justify-end space-x-3 mt-6">
                  <button
                    onClick={() => setShowEditModal(false)}
                    className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
                  >
                    取消
                  </button>
                  <button
                    onClick={handleUpdateUser}
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
                  >
                    保存
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UserManagement; 
import React, { useState, useEffect } from 'react';
import { userAPI, locationAPI, User, Province, City } from '../services/api';

interface ProfileEditProps {
  currentUser: User;
  onUpdate: (user: User) => void;
}

const ProfileEdit: React.FC<ProfileEditProps> = ({ currentUser, onUpdate }) => {
  const [form, setForm] = useState({
    username: currentUser.username || '',
    email: currentUser.email || '',
    phone: currentUser.phone || '',
    real_name: currentUser.real_name || '',
    age: currentUser.age?.toString() || '',
    grade: currentUser.grade || '',
    province_id: currentUser.province_id?.toString() || '',
    city_id: currentUser.city_id?.toString() || '',
    password: '',
    confirmPassword: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [provinces, setProvinces] = useState<{id:number, name:string}[]>([]);
  const [cities, setCities] = useState<City[]>([]);
  const [loadingProvinces, setLoadingProvinces] = useState(true);
  const [loadingCities, setLoadingCities] = useState(false);

  useEffect(() => {
    setForm({
      username: currentUser.username || '',
      email: currentUser.email || '',
      phone: currentUser.phone || '',
      real_name: currentUser.real_name || '',
      age: currentUser.age?.toString() || '',
      grade: currentUser.grade || '',
      province_id: currentUser.province_id?.toString() || '',
      city_id: currentUser.city_id?.toString() || '',
      password: '',
      confirmPassword: ''
    });
  }, [currentUser]);

  useEffect(() => {
    loadProvinces();
  }, []);

  useEffect(() => {
    if (form.province_id) {
      loadCities(parseInt(form.province_id));
    } else {
      setCities([]);
      setForm(prev => ({ ...prev, city_id: '' }));
    }
  }, [form.province_id]);

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    // 验证密码确认
    if (form.password && form.password !== form.confirmPassword) {
      setError('两次输入的密码不一致');
      setLoading(false);
      return;
    }

    try {
      const updateData: any = { ...form };
      
      // 移除空值和确认密码字段
      delete updateData.confirmPassword;
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

      const updatedUser = await userAPI.updateUser(currentUser.id, updateData);
      console.log('✅ 个人信息更新成功');
      setSuccess('个人信息更新成功！');
      onUpdate(updatedUser);
      
      // 清空密码字段
      setForm(prev => ({
        ...prev,
        password: '',
        confirmPassword: ''
      }));
    } catch (err) {
      console.error('❌ 更新个人信息失败:', err);
      setError('更新个人信息失败，请检查输入信息');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="flex-1 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white shadow-lg rounded-lg overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-2xl font-bold text-gray-900">编辑个人信息</h2>
            <p className="mt-1 text-sm text-gray-600">更新您的个人信息和账户设置</p>
          </div>

          <form onSubmit={handleSubmit} className="px-6 py-6">
            {error && (
              <div className="mb-4 bg-red-50 border-l-4 border-red-400 p-4">
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

            {success && (
              <div className="mb-4 bg-green-50 border-l-4 border-green-400 p-4">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <p className="text-sm text-green-700">{success}</p>
                  </div>
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              <div>
                <label htmlFor="username" className="block text-sm font-medium text-gray-700">用户名</label>
                <input
                  id="username"
                  type="text"
                  value={form.username}
                  onChange={(e) => handleInputChange('username', e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">邮箱</label>
                <input
                  id="email"
                  type="email"
                  value={form.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="phone" className="block text-sm font-medium text-gray-700">手机号</label>
                <input
                  id="phone"
                  type="text"
                  value={form.phone}
                  onChange={(e) => handleInputChange('phone', e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label htmlFor="real_name" className="block text-sm font-medium text-gray-700">真实姓名</label>
                <input
                  id="real_name"
                  type="text"
                  value={form.real_name}
                  onChange={(e) => handleInputChange('real_name', e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label htmlFor="age" className="block text-sm font-medium text-gray-700">年龄</label>
                <input
                  id="age"
                  type="number"
                  value={form.age}
                  onChange={(e) => handleInputChange('age', e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  min="1"
                  max="120"
                />
              </div>

              <div>
                <label htmlFor="grade" className="block text-sm font-medium text-gray-700">年级</label>
                <select
                  id="grade"
                  value={form.grade}
                  onChange={(e) => handleInputChange('grade', e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">请选择年级</option>
                  <option value="高一">高一</option>
                  <option value="高二">高二</option>
                  <option value="高三">高三</option>
                  <option value="大一">大一</option>
                  <option value="大二">大二</option>
                  <option value="大三">大三</option>
                  <option value="大四">大四</option>
                </select>
              </div>

              <div>
                <label htmlFor="province_id" className="block text-sm font-medium text-gray-700">省份</label>
                <select
                  id="province_id"
                  value={form.province_id}
                  onChange={(e) => handleInputChange('province_id', e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  disabled={loadingProvinces}
                >
                  <option value="">请选择省份</option>
                  {(provinces || []).map((province) => (
                    <option key={province.id} value={province.id}>{province.name}</option>
                  ))}
                </select>
                {loadingProvinces && (
                  <p className="mt-1 text-sm text-gray-500">加载中...</p>
                )}
              </div>

              <div>
                <label htmlFor="city_id" className="block text-sm font-medium text-gray-700">城市</label>
                <select
                  id="city_id"
                  value={form.city_id}
                  onChange={(e) => handleInputChange('city_id', e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  disabled={!form.province_id || loadingCities}
                >
                  <option value="">请选择城市</option>
                  {(cities || []).map((city) => (
                    <option key={city.id} value={city.id}>
                      {city.name}
                    </option>
                  ))}
                </select>
                {loadingCities && (
                  <p className="mt-1 text-sm text-gray-500">加载中...</p>
                )}
              </div>
            </div>

            <div className="mt-6 border-t border-gray-200 pt-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">修改密码</h3>
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-gray-700">新密码</label>
                  <input
                    id="password"
                    type="password"
                    value={form.password}
                    onChange={(e) => handleInputChange('password', e.target.value)}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="留空表示不修改密码"
                  />
                </div>

                <div>
                  <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">确认新密码</label>
                  <input
                    id="confirmPassword"
                    type="password"
                    value={form.confirmPassword}
                    onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="再次输入新密码"
                  />
                </div>
              </div>
            </div>

            <div className="mt-6 flex justify-end space-x-3">
              <button
                type="submit"
                disabled={loading}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? '保存中...' : '保存更改'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ProfileEdit; 
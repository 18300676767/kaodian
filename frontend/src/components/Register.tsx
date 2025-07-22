import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI, locationAPI, Province, City } from '../services/api';

const Register: React.FC = () => {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone: '',
    real_name: '',
    age: '',
    grade: '',
    province_id: '',
    city_id: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [provinces, setProvinces] = useState<Province[]>([]);
  const [cities, setCities] = useState<City[]>([]);
  const [loadingProvinces, setLoadingProvinces] = useState(true);
  const [loadingCities, setLoadingCities] = useState(false);
  const navigate = useNavigate();

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

    // 验证密码确认
    if (form.password !== form.confirmPassword) {
      setError('两次输入的密码不一致');
      setLoading(false);
      return;
    }

    try {
      const registerData: any = { ...form };
      
      // 移除确认密码字段
      delete registerData.confirmPassword;
      
      // 移除空值
      Object.keys(registerData).forEach(key => {
        if (registerData[key] === '') {
          delete registerData[key];
        }
      });

      // 转换数字字段
      if (registerData.age) {
        registerData.age = parseInt(registerData.age);
      }
      if (registerData.province_id) {
        registerData.province_id = parseInt(registerData.province_id);
      }
      if (registerData.city_id) {
        registerData.city_id = parseInt(registerData.city_id);
      }

      await authAPI.register(registerData);
      console.log('✅ 注册成功');
      alert('🎉 注册成功！请登录');
      navigate('/login');
    } catch (err: any) {
      console.error('❌ 注册失败:', err);
      setError(err.response?.data?.detail || '注册失败，请检查输入信息');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          注册账户
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          已有账户？
          <Link to="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
            立即登录
          </Link>
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <form className="space-y-6" onSubmit={handleSubmit}>
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

            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              <div>
                <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                  用户名
                </label>
                <div className="mt-1">
                  <input
                    id="username"
                    name="username"
                    type="text"
                    required
                    value={form.username}
                    onChange={(e) => handleInputChange('username', e.target.value)}
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                  邮箱
                </label>
                <div className="mt-1">
                  <input
                    id="email"
                    name="email"
                    type="email"
                    required
                    value={form.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                  密码
                </label>
                <div className="mt-1">
                  <input
                    id="password"
                    name="password"
                    type="password"
                    required
                    value={form.password}
                    onChange={(e) => handleInputChange('password', e.target.value)}
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                  确认密码
                </label>
                <div className="mt-1">
                  <input
                    id="confirmPassword"
                    name="confirmPassword"
                    type="password"
                    required
                    value={form.confirmPassword}
                    onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
                  手机号
                </label>
                <div className="mt-1">
                  <input
                    id="phone"
                    name="phone"
                    type="text"
                    value={form.phone}
                    onChange={(e) => handleInputChange('phone', e.target.value)}
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="real_name" className="block text-sm font-medium text-gray-700">
                  真实姓名
                </label>
                <div className="mt-1">
                  <input
                    id="real_name"
                    name="real_name"
                    type="text"
                    value={form.real_name}
                    onChange={(e) => handleInputChange('real_name', e.target.value)}
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="age" className="block text-sm font-medium text-gray-700">
                  年龄
                </label>
                <div className="mt-1">
                  <input
                    id="age"
                    name="age"
                    type="number"
                    min="1"
                    max="120"
                    value={form.age}
                    onChange={(e) => handleInputChange('age', e.target.value)}
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="grade" className="block text-sm font-medium text-gray-700">
                  年级
                </label>
                <div className="mt-1">
                  <select
                    id="grade"
                    name="grade"
                    value={form.grade}
                    onChange={(e) => handleInputChange('grade', e.target.value)}
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
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
              </div>

              <div>
                <label htmlFor="province_id" className="block text-sm font-medium text-gray-700">
                  省份
                </label>
                <div className="mt-1">
                  <select
                    id="province_id"
                    name="province_id"
                    value={form.province_id}
                    onChange={(e) => handleInputChange('province_id', e.target.value)}
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    disabled={loadingProvinces}
                  >
                    <option value="">请选择省份</option>
                    {provinces.map((province) => (
                      <option key={province.id} value={province.id}>
                        {province.name}
                      </option>
                    ))}
                  </select>
                  {loadingProvinces && (
                    <p className="mt-1 text-sm text-gray-500">加载中...</p>
                  )}
                </div>
              </div>

              <div>
                <label htmlFor="city_id" className="block text-sm font-medium text-gray-700">
                  城市
                </label>
                <div className="mt-1">
                  <select
                    id="city_id"
                    name="city_id"
                    value={form.city_id}
                    onChange={(e) => handleInputChange('city_id', e.target.value)}
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    disabled={!form.province_id || loadingCities}
                  >
                    <option value="">请选择城市</option>
                    {cities.map((city) => (
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
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? '注册中...' : '注册'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Register; 
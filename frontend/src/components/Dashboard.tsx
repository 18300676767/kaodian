import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI, User } from '../services/api';
import UserManagement from './UserManagement';
import ProfileEdit from './ProfileEdit';
import ExamPointManagement from './ExamPointManagement';
import ExamPaperManagement from './ExamPaperManagement';

type DashboardView = 'home' | 'user-management' | 'profile-edit' | 'exam-point-management' | 'exam-paper-management';

const Dashboard: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [currentView, setCurrentView] = useState<DashboardView>('home');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    const fetchUser = async () => {
      try {
        const userData = await authAPI.getCurrentUser();
        setUser(userData);
        console.log('✅ 获取用户信息成功');
      } catch (error) {
        console.error('❌ 获取用户信息失败:', error);
        localStorage.removeItem('token');
        navigate('/login');
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    console.log('✅ 已退出登录');
    alert('👋 已成功退出登录');
    navigate('/login');
  };

  const handleProfileUpdate = (updatedUser: User) => {
    setUser(updatedUser);
    console.log('✅ 用户信息已更新');
  };

  const renderNavigation = () => (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center">
              <svg className="h-8 w-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              <span className="ml-2 text-xl font-bold text-gray-900">高考考点分析系统</span>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-gray-700">欢迎，{user?.username}</span>
            <button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              退出登录
            </button>
          </div>
        </div>
      </div>
    </nav>
  );

  const renderSidebar = () => (
    <div className="w-64 bg-white shadow-sm border-r">
      <div className="p-4">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">功能菜单</h2>
        <nav className="space-y-2">
          <button
            onClick={() => setCurrentView('home')}
            className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium ${
              currentView === 'home'
                ? 'bg-indigo-100 text-indigo-700'
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
            }`}
          >
            <div className="flex items-center">
              <svg className="mr-3 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5a2 2 0 012-2h4a2 2 0 012 2v6H8V5z" />
              </svg>
              系统概览
            </div>
          </button>
          
          <button
            onClick={() => setCurrentView('user-management')}
            className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium ${
              currentView === 'user-management'
                ? 'bg-indigo-100 text-indigo-700'
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
            }`}
          >
            <div className="flex items-center">
              <svg className="mr-3 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
              </svg>
              用户管理
            </div>
          </button>
          
          <button
            onClick={() => setCurrentView('profile-edit')}
            className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium ${
              currentView === 'profile-edit'
                ? 'bg-indigo-100 text-indigo-700'
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
            }`}
          >
            <div className="flex items-center">
              <svg className="mr-3 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              个人信息
            </div>
          </button>
          
          <button
            onClick={() => setCurrentView('exam-point-management')}
            className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium ${
              currentView === 'exam-point-management'
                ? 'bg-indigo-100 text-indigo-700'
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
            }`}
          >
            <div className="flex items-center">
              <svg className="mr-3 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              考点管理
            </div>
          </button>

          <button
            onClick={() => setCurrentView('exam-paper-management')}
            className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium ${
              currentView === 'exam-paper-management'
                ? 'bg-indigo-100 text-indigo-700'
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
            }`}
          >
            <div className="flex items-center">
              <svg className="mr-3 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              高考试题管理
            </div>
          </button>
        </nav>
      </div>
    </div>
  );

  const renderHomeView = () => (
    <div className="flex-1 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">系统概览</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {/* 用户信息卡片 */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-12 w-12 rounded-full bg-indigo-500 flex items-center justify-center">
                  <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">用户信息</h3>
                <p className="text-sm text-gray-500">查看和管理个人信息</p>
              </div>
            </div>
            <div className="mt-4">
              <button
                onClick={() => setCurrentView('profile-edit')}
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                编辑个人信息
              </button>
            </div>
          </div>

          {/* 用户管理卡片 */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-12 w-12 rounded-full bg-green-500 flex items-center justify-center">
                  <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                  </svg>
                </div>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">用户管理</h3>
                <p className="text-sm text-gray-500">管理系统中的所有用户</p>
              </div>
            </div>
            <div className="mt-4">
              <button
                onClick={() => setCurrentView('user-management')}
                className="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                进入用户管理
              </button>
            </div>
          </div>

          {/* 考点管理卡片 */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-12 w-12 rounded-full bg-purple-500 flex items-center justify-center">
                  <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">考点管理</h3>
                <p className="text-sm text-gray-500">管理高考考点信息</p>
              </div>
            </div>
            <div className="mt-4">
              <button
                onClick={() => setCurrentView('exam-point-management')}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                进入考点管理
              </button>
            </div>
          </div>

          {/* 高考试题管理卡片 */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-12 w-12 rounded-full bg-yellow-500 flex items-center justify-center">
                  <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">高考试题管理</h3>
                <p className="text-sm text-gray-500">管理高考试题、编辑、导入导出等</p>
              </div>
            </div>
            <div className="mt-4">
              <button
                onClick={() => setCurrentView('exam-paper-management')}
                className="w-full bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                进入高考试题管理
              </button>
            </div>
          </div>
        </div>

        {/* 当前用户信息 */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">当前用户信息</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm font-medium text-gray-500">用户名</p>
              <p className="text-sm text-gray-900">{user?.username}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">邮箱</p>
              <p className="text-sm text-gray-900">{user?.email}</p>
            </div>
            {user?.real_name && (
              <div>
                <p className="text-sm font-medium text-gray-500">真实姓名</p>
                <p className="text-sm text-gray-900">{user.real_name}</p>
              </div>
            )}
            {user?.phone && (
              <div>
                <p className="text-sm font-medium text-gray-500">手机号</p>
                <p className="text-sm text-gray-900">{user.phone}</p>
              </div>
            )}
            {user?.age && (
              <div>
                <p className="text-sm font-medium text-gray-500">年龄</p>
                <p className="text-sm text-gray-900">{user.age}岁</p>
              </div>
            )}
            {user?.grade && (
              <div>
                <p className="text-sm font-medium text-gray-500">年级</p>
                <p className="text-sm text-gray-900">{user.grade}</p>
              </div>
            )}
            {user?.province && user?.city && (
              <div>
                <p className="text-sm font-medium text-gray-500">地区</p>
                <p className="text-sm text-gray-900">{user.province.name} {user.city.name}</p>
              </div>
            )}
            <div>
              <p className="text-sm font-medium text-gray-500">注册时间</p>
              <p className="text-sm text-gray-900">
                {user?.created_at ? new Date(user.created_at).toLocaleString() : '未知'}
              </p>
            </div>
          </div>
        </div>

        {/* 在概览卡片区添加高考试题管理 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
          {/* 用户信息、用户管理、考点管理卡片 ... */}
          {/* 这里的考点管理和高考试题管理卡片已上移并合并到主卡片区，无需重复显示，可删除此区块 */}
        </div>
      </div>
    </div>
  );

  const renderContent = () => {
    switch (currentView) {
      case 'user-management':
        return user ? <UserManagement currentUser={user} /> : null;
      case 'profile-edit':
        return user ? <ProfileEdit currentUser={user} onUpdate={handleProfileUpdate} /> : null;
      case 'exam-point-management':
        return user ? <ExamPointManagement currentUser={user} /> : null;
      case 'exam-paper-management':
        return user ? <ExamPaperManagement currentUser={user} /> : null;
      default:
        return renderHomeView();
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <svg className="animate-spin h-12 w-12 text-indigo-600 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p className="mt-4 text-gray-600">加载中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {renderNavigation()}
      <div className="flex">
        {renderSidebar()}
        <main className="flex-1">
          {renderContent()}
        </main>
      </div>
    </div>
  );
};

export default Dashboard; 
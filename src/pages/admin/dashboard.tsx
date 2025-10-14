import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../../lib/api';

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await authAPI.getMe();
      if (response.success && response.data?.user.isAdmin) {
        setUser(response.data.user);
      } else {
        alert('관리자 권한이 필요합니다');
        navigate('/auth/login');
      }
    } catch (error) {
      alert('로그인이 필요합니다');
      navigate('/auth/login');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    authAPI.logout();
    navigate('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">로딩 중...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {/* 헤더 */}
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-pink-400">오피인포 관리자</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-300">
                <i className="ri-user-line mr-2"></i>
                {user?.username} ({user?.role})
              </span>
              <button
                onClick={handleLogout}
                className="bg-gray-700 text-white px-4 py-2 rounded-lg hover:bg-gray-600 transition-colors"
              >
                <i className="ri-logout-box-line mr-2"></i>
                로그아웃
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 통계 카드 */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">전체 업체</p>
                <p className="text-3xl font-bold text-white mt-2">71</p>
              </div>
              <div className="bg-pink-500/20 p-3 rounded-lg">
                <i className="ri-store-2-line text-3xl text-pink-400"></i>
              </div>
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">전체 회원</p>
                <p className="text-3xl font-bold text-white mt-2">1</p>
              </div>
              <div className="bg-blue-500/20 p-3 rounded-lg">
                <i className="ri-user-line text-3xl text-blue-400"></i>
              </div>
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">지역 수</p>
                <p className="text-3xl font-bold text-white mt-2">7</p>
              </div>
              <div className="bg-green-500/20 p-3 rounded-lg">
                <i className="ri-map-pin-line text-3xl text-green-400"></i>
              </div>
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">카테고리</p>
                <p className="text-3xl font-bold text-white mt-2">5</p>
              </div>
              <div className="bg-purple-500/20 p-3 rounded-lg">
                <i className="ri-dashboard-line text-3xl text-purple-400"></i>
              </div>
            </div>
          </div>
        </div>

        {/* 메뉴 그리드 */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link
            to="/admin/shops"
            className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-pink-400 transition-colors group"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-white group-hover:text-pink-400 transition-colors">
                업체 관리
              </h3>
              <i className="ri-store-2-line text-3xl text-pink-400"></i>
            </div>
            <p className="text-gray-400">업체 등록, 수정, 삭제</p>
          </Link>

          <Link
            to="/admin/users"
            className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-blue-400 transition-colors group"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-white group-hover:text-blue-400 transition-colors">
                회원 관리
              </h3>
              <i className="ri-user-settings-line text-3xl text-blue-400"></i>
            </div>
            <p className="text-gray-400">회원 목록, 권한 관리</p>
          </Link>

          <Link
            to="/admin/categories"
            className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-green-400 transition-colors group"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-white group-hover:text-green-400 transition-colors">
                카테고리 관리
              </h3>
              <i className="ri-price-tag-3-line text-3xl text-green-400"></i>
            </div>
            <p className="text-gray-400">카테고리 설정</p>
          </Link>

          <Link
            to="/admin/regions"
            className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-yellow-400 transition-colors group"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-white group-hover:text-yellow-400 transition-colors">
                지역 관리
              </h3>
              <i className="ri-map-2-line text-3xl text-yellow-400"></i>
            </div>
            <p className="text-gray-400">지역 설정 및 관리</p>
          </Link>

          <Link
            to="/admin/settings"
            className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-purple-400 transition-colors group"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-white group-hover:text-purple-400 transition-colors">
                사이트 설정
              </h3>
              <i className="ri-settings-3-line text-3xl text-purple-400"></i>
            </div>
            <p className="text-gray-400">사이트 전체 설정</p>
          </Link>

          <Link
            to="/"
            className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-gray-400 transition-colors group"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-white group-hover:text-gray-400 transition-colors">
                메인 페이지
              </h3>
              <i className="ri-home-4-line text-3xl text-gray-400"></i>
            </div>
            <p className="text-gray-400">사용자 페이지로 이동</p>
          </Link>
        </div>

        {/* 최근 활동 */}
        <div className="mt-8 bg-gray-800 rounded-lg p-6 border border-gray-700">
          <h3 className="text-xl font-semibold text-white mb-4">
            <i className="ri-history-line mr-2"></i>
            최근 활동
          </h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between py-3 border-b border-gray-700">
              <div className="flex items-center">
                <div className="bg-green-500/20 p-2 rounded-lg mr-3">
                  <i className="ri-user-add-line text-green-400"></i>
                </div>
                <div>
                  <p className="text-white">관리자 계정 생성</p>
                  <p className="text-sm text-gray-400">admin</p>
                </div>
              </div>
              <span className="text-sm text-gray-400">방금 전</span>
            </div>

            <div className="flex items-center justify-between py-3 border-b border-gray-700">
              <div className="flex items-center">
                <div className="bg-blue-500/20 p-2 rounded-lg mr-3">
                  <i className="ri-database-2-line text-blue-400"></i>
                </div>
                <div>
                  <p className="text-white">데이터베이스 설정 완료</p>
                  <p className="text-sm text-gray-400">SQLite</p>
                </div>
              </div>
              <span className="text-sm text-gray-400">1분 전</span>
            </div>

            <div className="flex items-center justify-between py-3">
              <div className="flex items-center">
                <div className="bg-pink-500/20 p-2 rounded-lg mr-3">
                  <i className="ri-upload-cloud-line text-pink-400"></i>
                </div>
                <div>
                  <p className="text-white">업체 데이터 업로드</p>
                  <p className="text-sm text-gray-400">71개 업체</p>
                </div>
              </div>
              <span className="text-sm text-gray-400">10분 전</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

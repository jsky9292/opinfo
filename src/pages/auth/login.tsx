import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../../lib/api';

export default function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authAPI.login(formData);

      if (response.success) {
        // 로그인 성공
        alert(`${response.data?.user.username}님, 환영합니다!`);
        navigate('/');
      }
    } catch (err: any) {
      setError(err.message || '로그인에 실패했습니다. 다시 시도해주세요.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        {/* 로고 */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-pink-400 mb-2">오피인포</h1>
          <p className="text-gray-400">로그인하여 더 많은 정보를 확인하세요</p>
        </div>

        {/* 로그인 폼 */}
        <div className="bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* 아이디 */}
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-300 mb-2">
                아이디
              </label>
              <input
                type="text"
                id="username"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-pink-400 focus:ring-1 focus:ring-pink-400"
                placeholder="아이디를 입력하세요"
                required
              />
            </div>

            {/* 비밀번호 */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                비밀번호
              </label>
              <input
                type="password"
                id="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-pink-400 focus:ring-1 focus:ring-pink-400"
                placeholder="비밀번호를 입력하세요"
                required
              />
            </div>

            {/* 에러 메시지 */}
            {error && (
              <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded-lg text-sm">
                {error}
              </div>
            )}

            {/* 로그인 버튼 */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-pink-500 text-white py-3 px-4 rounded-lg font-medium hover:bg-pink-600 focus:outline-none focus:ring-2 focus:ring-pink-400 focus:ring-offset-2 focus:ring-offset-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? '로그인 중...' : '로그인'}
            </button>
          </form>

          {/* 추가 링크 */}
          <div className="mt-6 space-y-3">
            <div className="flex items-center justify-between text-sm">
              <Link to="/auth/signup" className="text-pink-400 hover:text-pink-300">
                회원가입
              </Link>
              <Link to="/auth/find-password" className="text-gray-400 hover:text-gray-300">
                비밀번호 찾기
              </Link>
            </div>

            <div className="border-t border-gray-700 pt-4">
              <Link
                to="/"
                className="block text-center text-gray-400 hover:text-gray-300 text-sm"
              >
                <i className="ri-arrow-left-line mr-1"></i>
                메인으로 돌아가기
              </Link>
            </div>
          </div>
        </div>

        {/* 소셜 로그인 (선택사항) */}
        <div className="mt-6">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-700"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-gray-900 text-gray-400">또는</span>
            </div>
          </div>

          <div className="mt-6 grid grid-cols-2 gap-3">
            <button
              type="button"
              className="w-full bg-yellow-500 text-gray-900 py-3 px-4 rounded-lg font-medium hover:bg-yellow-400 transition-colors flex items-center justify-center"
            >
              <i className="ri-kakao-talk-fill mr-2"></i>
              카카오
            </button>
            <button
              type="button"
              className="w-full bg-green-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-green-500 transition-colors flex items-center justify-center"
            >
              <i className="ri-chat-1-fill mr-2"></i>
              네이버
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

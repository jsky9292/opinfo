import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../../lib/api';

export default function Signup() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    passwordConfirm: '',
    email: '',
    agreeTerms: false,
    agreePrivacy: false
  });
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [loading, setLoading] = useState(false);

  const validateForm = () => {
    const newErrors: { [key: string]: string } = {};

    // 아이디 검증
    if (formData.username.length < 4) {
      newErrors.username = '아이디는 4자 이상이어야 합니다';
    }

    // 비밀번호 검증
    if (formData.password.length < 8) {
      newErrors.password = '비밀번호는 8자 이상이어야 합니다';
    }

    // 비밀번호 확인
    if (formData.password !== formData.passwordConfirm) {
      newErrors.passwordConfirm = '비밀번호가 일치하지 않습니다';
    }

    // 이메일 검증
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      newErrors.email = '올바른 이메일 형식이 아닙니다';
    }

    // 약관 동의 검증
    if (!formData.agreeTerms) {
      newErrors.agreeTerms = '이용약관에 동의해주세요';
    }
    if (!formData.agreePrivacy) {
      newErrors.agreePrivacy = '개인정보 처리방침에 동의해주세요';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const response = await authAPI.signup({
        username: formData.username,
        email: formData.email,
        password: formData.password,
      });

      if (response.success) {
        alert('회원가입이 완료되었습니다!');
        navigate('/');
      }
    } catch (err: any) {
      setErrors({ ...errors, submit: err.message || '회원가입에 실패했습니다. 다시 시도해주세요.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 py-12 px-4">
      <div className="max-w-md mx-auto">
        {/* 로고 */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-pink-400 mb-2">오피인포</h1>
          <p className="text-gray-400">간편하게 가입하고 시작하세요</p>
        </div>

        {/* 회원가입 폼 */}
        <div className="bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700">
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* 아이디 */}
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-300 mb-2">
                아이디 <span className="text-pink-400">*</span>
              </label>
              <input
                type="text"
                id="username"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-pink-400 focus:ring-1 focus:ring-pink-400"
                placeholder="4자 이상 입력하세요"
                required
              />
              {errors.username && (
                <p className="mt-1 text-sm text-red-400">{errors.username}</p>
              )}
            </div>

            {/* 이메일 */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                이메일 <span className="text-pink-400">*</span>
              </label>
              <input
                type="email"
                id="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-pink-400 focus:ring-1 focus:ring-pink-400"
                placeholder="example@email.com"
                required
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-400">{errors.email}</p>
              )}
            </div>

            {/* 비밀번호 */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                비밀번호 <span className="text-pink-400">*</span>
              </label>
              <input
                type="password"
                id="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-pink-400 focus:ring-1 focus:ring-pink-400"
                placeholder="8자 이상 입력하세요"
                required
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-400">{errors.password}</p>
              )}
            </div>

            {/* 비밀번호 확인 */}
            <div>
              <label htmlFor="passwordConfirm" className="block text-sm font-medium text-gray-300 mb-2">
                비밀번호 확인 <span className="text-pink-400">*</span>
              </label>
              <input
                type="password"
                id="passwordConfirm"
                value={formData.passwordConfirm}
                onChange={(e) => setFormData({ ...formData, passwordConfirm: e.target.value })}
                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-pink-400 focus:ring-1 focus:ring-pink-400"
                placeholder="비밀번호를 다시 입력하세요"
                required
              />
              {errors.passwordConfirm && (
                <p className="mt-1 text-sm text-red-400">{errors.passwordConfirm}</p>
              )}
            </div>

            {/* 약관 동의 */}
            <div className="space-y-3 pt-4 border-t border-gray-700">
              <div className="flex items-start">
                <input
                  type="checkbox"
                  id="agreeTerms"
                  checked={formData.agreeTerms}
                  onChange={(e) => setFormData({ ...formData, agreeTerms: e.target.checked })}
                  className="mt-1 w-4 h-4 bg-gray-700 border-gray-600 rounded text-pink-500 focus:ring-pink-400 focus:ring-offset-gray-800"
                />
                <label htmlFor="agreeTerms" className="ml-3 text-sm text-gray-300">
                  <span className="text-pink-400">*</span> 이용약관에 동의합니다
                  <a href="#" className="text-pink-400 hover:text-pink-300 ml-2">(보기)</a>
                </label>
              </div>
              {errors.agreeTerms && (
                <p className="ml-7 text-sm text-red-400">{errors.agreeTerms}</p>
              )}

              <div className="flex items-start">
                <input
                  type="checkbox"
                  id="agreePrivacy"
                  checked={formData.agreePrivacy}
                  onChange={(e) => setFormData({ ...formData, agreePrivacy: e.target.checked })}
                  className="mt-1 w-4 h-4 bg-gray-700 border-gray-600 rounded text-pink-500 focus:ring-pink-400 focus:ring-offset-gray-800"
                />
                <label htmlFor="agreePrivacy" className="ml-3 text-sm text-gray-300">
                  <span className="text-pink-400">*</span> 개인정보 처리방침에 동의합니다
                  <a href="#" className="text-pink-400 hover:text-pink-300 ml-2">(보기)</a>
                </label>
              </div>
              {errors.agreePrivacy && (
                <p className="ml-7 text-sm text-red-400">{errors.agreePrivacy}</p>
              )}
            </div>

            {/* 전체 에러 메시지 */}
            {errors.submit && (
              <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded-lg text-sm">
                {errors.submit}
              </div>
            )}

            {/* 회원가입 버튼 */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-pink-500 text-white py-3 px-4 rounded-lg font-medium hover:bg-pink-600 focus:outline-none focus:ring-2 focus:ring-pink-400 focus:ring-offset-2 focus:ring-offset-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? '가입 중...' : '회원가입'}
            </button>
          </form>

          {/* 추가 링크 */}
          <div className="mt-6 text-center text-sm">
            <span className="text-gray-400">이미 계정이 있으신가요?</span>
            <Link to="/auth/login" className="ml-2 text-pink-400 hover:text-pink-300">
              로그인
            </Link>
          </div>

          <div className="mt-4 border-t border-gray-700 pt-4">
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
    </div>
  );
}

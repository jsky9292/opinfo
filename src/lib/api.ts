// API 클라이언트
const API_URL = 'http://localhost:5000/api';

interface LoginRequest {
  username: string;
  password: string;
}

interface SignupRequest {
  username: string;
  email: string;
  password: string;
  phone?: string;
}

interface AuthResponse {
  success: boolean;
  message: string;
  data?: {
    token: string;
    user: {
      id: number;
      username: string;
      email: string;
      role: string;
      isAdmin: boolean;
    };
  };
}

export const authAPI = {
  // 로그인
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || '로그인에 실패했습니다');
    }

    // 토큰 저장
    if (result.data?.token) {
      localStorage.setItem('token', result.data.token);
      localStorage.setItem('user', JSON.stringify(result.data.user));
    }

    return result;
  },

  // 회원가입
  signup: async (data: SignupRequest): Promise<AuthResponse> => {
    const response = await fetch(`${API_URL}/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || '회원가입에 실패했습니다');
    }

    // 토큰 저장
    if (result.data?.token) {
      localStorage.setItem('token', result.data.token);
      localStorage.setItem('user', JSON.stringify(result.data.user));
    }

    return result;
  },

  // 사용자 정보 조회
  getMe: async (): Promise<AuthResponse> => {
    const token = localStorage.getItem('token');

    if (!token) {
      throw new Error('인증 토큰이 없습니다');
    }

    const response = await fetch(`${API_URL}/auth/me`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    const result = await response.json();

    if (!response.ok) {
      // 토큰이 만료된 경우 로그아웃
      if (response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
      throw new Error(result.message || '사용자 정보를 가져올 수 없습니다');
    }

    return result;
  },

  // 로그아웃
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  // 현재 사용자 확인
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  // 로그인 여부 확인
  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },
};

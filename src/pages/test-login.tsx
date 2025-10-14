import { useState } from 'react';

export default function TestLogin() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [result, setResult] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setResult('로그인 시도 중...');

    try {
      const response = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (error: any) {
      setResult('에러: ' + error.message);
    }
  };

  return (
    <div style={{ padding: '20px', backgroundColor: '#1a1a1a', minHeight: '100vh', color: 'white' }}>
      <h1>로그인 테스트</h1>

      <form onSubmit={handleLogin} style={{ maxWidth: '400px', marginTop: '20px' }}>
        <div style={{ marginBottom: '10px' }}>
          <label>아이디:</label>
          <br />
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ width: '100%', padding: '8px', fontSize: '16px' }}
            placeholder="admin"
          />
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label>비밀번호:</label>
          <br />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: '100%', padding: '8px', fontSize: '16px' }}
            placeholder="admin12345"
          />
        </div>

        <button
          type="submit"
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: '#ec4899',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          로그인 테스트
        </button>
      </form>

      {result && (
        <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#333', borderRadius: '4px' }}>
          <h3>결과:</h3>
          <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>{result}</pre>
        </div>
      )}

      <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#2a2a2a', borderRadius: '4px' }}>
        <h3>테스트 정보:</h3>
        <p>백엔드 서버: http://localhost:5000</p>
        <p>테스트 계정: admin / admin12345</p>
      </div>
    </div>
  );
}

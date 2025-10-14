import bcrypt from 'bcryptjs';
import { getDB } from '../config/db.js';

class User {
  // 사용자 생성
  static async create({ username, email, password, phone = '', role = 'user' }) {
    const db = getDB();

    // 비밀번호 해싱
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    try {
      const stmt = db.prepare(`
        INSERT INTO users (username, email, password, phone, role)
        VALUES (?, ?, ?, ?, ?)
      `);

      const result = stmt.run(username, email, hashedPassword, phone, role);

      return {
        id: result.lastInsertRowid,
        username,
        email,
        role,
        phone,
      };
    } catch (error) {
      if (error.message.includes('UNIQUE constraint failed')) {
        if (error.message.includes('username')) {
          throw new Error('이미 사용 중인 아이디입니다');
        }
        if (error.message.includes('email')) {
          throw new Error('이미 사용 중인 이메일입니다');
        }
      }
      throw error;
    }
  }

  // 사용자명으로 조회
  static findByUsername(username, includePassword = false) {
    const db = getDB();
    const stmt = db.prepare(`
      SELECT ${includePassword ? '*' : 'id, username, email, role, phone, created_at, last_login'}
      FROM users WHERE username = ?
    `);
    return stmt.get(username);
  }

  // 이메일로 조회
  static findByEmail(email) {
    const db = getDB();
    const stmt = db.prepare('SELECT * FROM users WHERE email = ?');
    return stmt.get(email);
  }

  // ID로 조회
  static findById(id) {
    const db = getDB();
    const stmt = db.prepare(`
      SELECT id, username, email, role, phone, created_at, last_login
      FROM users WHERE id = ?
    `);
    return stmt.get(id);
  }

  // 비밀번호 비교
  static async comparePassword(plainPassword, hashedPassword) {
    return await bcrypt.compare(plainPassword, hashedPassword);
  }

  // 마지막 로그인 시간 업데이트
  static updateLastLogin(userId) {
    const db = getDB();
    const stmt = db.prepare(`
      UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
    `);
    stmt.run(userId);
  }

  // 관리자 권한 확인
  static isAdmin(role) {
    return role === 'admin' || role === 'superadmin';
  }

  static isSuperAdmin(role) {
    return role === 'superadmin';
  }
}

export default User;

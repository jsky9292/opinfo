import Database from 'better-sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// SQLite 데이터베이스 파일 경로
const dbPath = path.join(__dirname, '..', 'database', 'opinfo.db');

let db = null;

export const connectDB = () => {
  try {
    db = new Database(dbPath, { verbose: console.log });

    // 테이블 생성
    db.exec(`
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        phone TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_login DATETIME
      );

      CREATE INDEX IF NOT EXISTS idx_username ON users(username);
      CREATE INDEX IF NOT EXISTS idx_email ON users(email);
    `);

    console.log('✅ SQLite Database Connected');
    return db;
  } catch (error) {
    console.error('❌ SQLite Connection Error:', error.message);
    process.exit(1);
  }
};

export const getDB = () => {
  if (!db) {
    return connectDB();
  }
  return db;
};

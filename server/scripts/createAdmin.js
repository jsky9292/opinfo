import dotenv from 'dotenv';
import User from '../models/User.js';
import { connectDB } from '../config/db.js';

dotenv.config();

const createAdminUser = async () => {
  try {
    // 데이터베이스 연결
    connectDB();

    // 기존 관리자 계정 확인
    const existingAdmin = User.findByUsername('admin');

    if (existingAdmin) {
      console.log('⚠️  관리자 계정이 이미 존재합니다');
      console.log('   Username: admin');
      process.exit(0);
    }

    // 관리자 계정 생성
    const adminUser = await User.create({
      username: 'admin',
      email: 'admin@opinfo.com',
      password: 'admin12345',
      role: 'admin',
      phone: '010-0000-0000',
    });

    console.log('✅ 관리자 계정이 생성되었습니다');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('   Username: admin');
    console.log('   Password: admin12345');
    console.log('   Email: admin@opinfo.com');
    console.log('   Role: admin');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('💡 보안을 위해 반드시 비밀번호를 변경해주세요');

    process.exit(0);
  } catch (error) {
    console.error('❌ 관리자 계정 생성 실패:', error.message);
    process.exit(1);
  }
};

createAdminUser();

import express from 'express';
import jwt from 'jsonwebtoken';
import { body, validationResult } from 'express-validator';
import User from '../models/User.js';

const router = express.Router();

// JWT 토큰 생성 함수
const generateToken = (userId) => {
  return jwt.sign({ id: userId }, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRE || '7d',
  });
};

// 회원가입
router.post('/signup', [
  body('username').isLength({ min: 4 }).withMessage('아이디는 4자 이상이어야 합니다'),
  body('email').isEmail().withMessage('올바른 이메일 형식이 아닙니다'),
  body('password').isLength({ min: 8 }).withMessage('비밀번호는 8자 이상이어야 합니다'),
], async (req, res) => {
  try {
    // 유효성 검사
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: errors.array()[0].msg
      });
    }

    const { username, email, password, phone } = req.body;

    // 새 사용자 생성
    const user = await User.create({
      username,
      email,
      password,
      phone: phone || '',
    });

    // 토큰 생성
    const token = generateToken(user.id);

    res.status(201).json({
      success: true,
      message: '회원가입이 완료되었습니다',
      data: {
        token,
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          role: user.role,
        },
      },
    });
  } catch (error) {
    console.error('Signup Error:', error);
    res.status(500).json({
      success: false,
      message: error.message || '회원가입 중 오류가 발생했습니다'
    });
  }
});

// 로그인
router.post('/login', [
  body('username').notEmpty().withMessage('아이디를 입력해주세요'),
  body('password').notEmpty().withMessage('비밀번호를 입력해주세요'),
], async (req, res) => {
  try {
    // 유효성 검사
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: errors.array()[0].msg
      });
    }

    const { username, password } = req.body;

    // 사용자 조회 (비밀번호 포함)
    const user = User.findByUsername(username, true);

    if (!user) {
      return res.status(401).json({
        success: false,
        message: '아이디 또는 비밀번호가 일치하지 않습니다'
      });
    }

    // 비밀번호 확인
    const isPasswordMatch = await User.comparePassword(password, user.password);

    if (!isPasswordMatch) {
      return res.status(401).json({
        success: false,
        message: '아이디 또는 비밀번호가 일치하지 않습니다'
      });
    }

    // 마지막 로그인 시간 업데이트
    User.updateLastLogin(user.id);

    // 토큰 생성
    const token = generateToken(user.id);

    res.json({
      success: true,
      message: '로그인 성공',
      data: {
        token,
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          role: user.role,
          isAdmin: User.isAdmin(user.role),
        },
      },
    });
  } catch (error) {
    console.error('Login Error:', error);
    res.status(500).json({
      success: false,
      message: '로그인 중 오류가 발생했습니다'
    });
  }
});

// 사용자 정보 조회 (인증 필요)
router.get('/me', async (req, res) => {
  try {
    // Authorization 헤더에서 토큰 추출
    const token = req.headers.authorization?.replace('Bearer ', '');

    if (!token) {
      return res.status(401).json({
        success: false,
        message: '인증 토큰이 필요합니다'
      });
    }

    // 토큰 검증
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = User.findById(decoded.id);

    if (!user) {
      return res.status(404).json({
        success: false,
        message: '사용자를 찾을 수 없습니다'
      });
    }

    res.json({
      success: true,
      data: {
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          role: user.role,
          phone: user.phone,
          isAdmin: User.isAdmin(user.role),
          createdAt: user.created_at,
          lastLogin: user.last_login,
        },
      },
    });
  } catch (error) {
    console.error('Auth Error:', error);
    res.status(401).json({
      success: false,
      message: '유효하지 않은 토큰입니다'
    });
  }
});

export default router;

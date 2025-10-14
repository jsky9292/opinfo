import mongoose from 'mongoose';

const shopSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  location: {
    type: String,
    required: true
  },
  district: {
    type: String,
    required: true
  },
  rating: {
    type: Number,
    default: 4.5,
    min: 0,
    max: 5
  },
  price: {
    type: String,
    default: '가격 문의'
  },
  services: [{
    type: String
  }],
  image: {
    type: String,
    default: 'https://dkxm8.com/img/temp_thum.jpg'
  },
  description: {
    type: String,
    default: ''
  },
  phone: {
    type: String,
    default: ''
  },
  address: {
    type: String,
    default: ''
  },
  hours: {
    type: String,
    default: ''
  },
  featured: {
    type: Boolean,
    default: false
  },
  category: {
    type: String,
    default: '기타'
  },
  gallery: [{
    type: String
  }],
  kakao_id: {
    type: String,
    default: ''
  },
  telegram_id: {
    type: String,
    default: ''
  },
  url: {
    type: String,
    default: ''
  },
  owner: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    default: null
  },
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true
});

// 인덱스 설정
shopSchema.index({ name: 'text', location: 'text', district: 'text' });
shopSchema.index({ location: 1 });
shopSchema.index({ category: 1 });
shopSchema.index({ owner: 1 });

export default mongoose.model('Shop', shopSchema);

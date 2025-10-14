import express from 'express';
import Shop from '../models/Shop.js';
import { protect, isOwnerOrAdmin, adminOnly } from '../middleware/auth.js';

const router = express.Router();

// @route   GET /api/shops
// @desc    Get all shops with filters and pagination
// @access  Public
router.get('/', async (req, res) => {
  try {
    const {
      location,
      district,
      category,
      search,
      page = 1,
      limit = 20,
      featured
    } = req.query;

    // Build query
    const query = { isActive: true };

    if (location) query.location = location;
    if (district) query.district = district;
    if (category) query.category = category;
    if (featured) query.featured = featured === 'true';

    // Text search
    if (search) {
      query.$text = { $search: search };
    }

    // Execute query with pagination
    const shops = await Shop.find(query)
      .limit(limit * 1)
      .skip((page - 1) * limit)
      .sort({ featured: -1, createdAt: -1 })
      .select('-__v');

    const count = await Shop.countDocuments(query);

    res.json({
      shops,
      totalPages: Math.ceil(count / limit),
      currentPage: page,
      total: count
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: '서버 오류가 발생했습니다.' });
  }
});

// @route   GET /api/shops/my
// @desc    Get current user's shops
// @access  Private
router.get('/my', protect, async (req, res) => {
  try {
    const shops = await Shop.find({ owner: req.user._id, isActive: true })
      .sort({ createdAt: -1 })
      .select('-__v');

    res.json(shops);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: '서버 오류가 발생했습니다.' });
  }
});

// @route   GET /api/shops/:id
// @desc    Get single shop by ID
// @access  Public
router.get('/:id', async (req, res) => {
  try {
    const shop = await Shop.findById(req.params.id)
      .populate('owner', 'name email')
      .select('-__v');

    if (!shop) {
      return res.status(404).json({ message: '업소를 찾을 수 없습니다.' });
    }

    res.json(shop);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: '서버 오류가 발생했습니다.' });
  }
});

// @route   POST /api/shops
// @desc    Create new shop
// @access  Private (Admin only)
router.post('/', protect, adminOnly, async (req, res) => {
  try {
    const {
      name,
      location,
      district,
      rating,
      price,
      services,
      image,
      description,
      phone,
      address,
      hours,
      category,
      gallery,
      kakao_id,
      telegram_id,
      url,
      owner,
      featured
    } = req.body;

    // Validate required fields
    if (!name || !location || !district) {
      return res.status(400).json({
        message: '업소명, 지역, 세부 지역은 필수 항목입니다.'
      });
    }

    const shop = await Shop.create({
      name,
      location,
      district,
      rating,
      price,
      services,
      image,
      description,
      phone,
      address,
      hours,
      category,
      gallery,
      kakao_id,
      telegram_id,
      url,
      owner: owner || null,
      featured: featured || false
    });

    res.status(201).json(shop);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: '서버 오류가 발생했습니다.' });
  }
});

// @route   PUT /api/shops/:id
// @desc    Update shop
// @access  Private (Owner or Admin)
router.put('/:id', protect, isOwnerOrAdmin(Shop), async (req, res) => {
  try {
    const {
      name,
      location,
      district,
      rating,
      price,
      services,
      image,
      description,
      phone,
      address,
      hours,
      category,
      gallery,
      kakao_id,
      telegram_id,
      url,
      featured
    } = req.body;

    const shop = await Shop.findById(req.params.id);

    if (!shop) {
      return res.status(404).json({ message: '업소를 찾을 수 없습니다.' });
    }

    // Update fields
    shop.name = name || shop.name;
    shop.location = location || shop.location;
    shop.district = district || shop.district;
    shop.rating = rating !== undefined ? rating : shop.rating;
    shop.price = price || shop.price;
    shop.services = services || shop.services;
    shop.image = image || shop.image;
    shop.description = description !== undefined ? description : shop.description;
    shop.phone = phone !== undefined ? phone : shop.phone;
    shop.address = address !== undefined ? address : shop.address;
    shop.hours = hours !== undefined ? hours : shop.hours;
    shop.category = category || shop.category;
    shop.gallery = gallery || shop.gallery;
    shop.kakao_id = kakao_id !== undefined ? kakao_id : shop.kakao_id;
    shop.telegram_id = telegram_id !== undefined ? telegram_id : shop.telegram_id;
    shop.url = url !== undefined ? url : shop.url;

    // Only admin can change featured status
    if (req.user.role === 'admin' && featured !== undefined) {
      shop.featured = featured;
    }

    await shop.save();

    res.json(shop);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: '서버 오류가 발생했습니다.' });
  }
});

// @route   DELETE /api/shops/:id
// @desc    Delete shop (soft delete)
// @access  Private (Owner or Admin)
router.delete('/:id', protect, isOwnerOrAdmin(Shop), async (req, res) => {
  try {
    const shop = await Shop.findById(req.params.id);

    if (!shop) {
      return res.status(404).json({ message: '업소를 찾을 수 없습니다.' });
    }

    // Soft delete
    shop.isActive = false;
    await shop.save();

    res.json({ message: '업소가 삭제되었습니다.' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: '서버 오류가 발생했습니다.' });
  }
});

// @route   GET /api/shops/stats/summary
// @desc    Get shop statistics
// @access  Private (Admin only)
router.get('/stats/summary', protect, adminOnly, async (req, res) => {
  try {
    const totalShops = await Shop.countDocuments({ isActive: true });
    const featuredShops = await Shop.countDocuments({ isActive: true, featured: true });

    const shopsByLocation = await Shop.aggregate([
      { $match: { isActive: true } },
      { $group: { _id: '$location', count: { $sum: 1 } } },
      { $sort: { count: -1 } }
    ]);

    const shopsByCategory = await Shop.aggregate([
      { $match: { isActive: true } },
      { $group: { _id: '$category', count: { $sum: 1 } } },
      { $sort: { count: -1 } }
    ]);

    res.json({
      totalShops,
      featuredShops,
      shopsByLocation,
      shopsByCategory
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: '서버 오류가 발생했습니다.' });
  }
});

export default router;

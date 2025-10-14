
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import shopsData from '../../data/shops_data.json';

interface MassageShop {
  id: number;
  name: string;
  location: string;
  district: string;
  rating: number;
  price: string;
  services: string[];
  image: string;
  description: string;
  phone: string;
  address: string;
  hours: string;
  featured: boolean;
  category: string;
  gallery: string[];
  detailDescription: string;
  amenities: string[];
  reviews: Review[];
  businessHours: BusinessHours;
  priceList: PriceItem[];
  therapists?: Therapist[];
  policies?: string[];
  kakao_id?: string;
  telegram_id?: string;
  url?: string;
}

interface BusinessHours {
  [key: string]: string;
}

interface PriceItem {
  service: string;
  duration: string;
  price: string;
  description: string;
}

interface Therapist {
  id: number;
  name: string;
  experience: string;
  specialty: string[];
  rating: number;
  image: string;
}

interface Review {
  id: number;
  userName: string;
  rating: number;
  comment: string;
  date: string;
  service: string;
  images?: string[];
}

const mockShop: MassageShop = {
  id: 1,
  name: "힐링 스파 센터",
  location: "서울",
  district: "강남구",
  rating: 4.8,
  price: "80,000원~",
  services: ["스웨디시", "아로마", "딥티슈"],
  image: "https://readdy.ai/api/search-image?query=Modern%20luxury%20spa%20interior%20with%20massage%20tables%2C%20soft%20lighting%2C%20clean%20white%20and%20beige%20colors%2C%20professional%20massage%20therapy%20room%20with%20relaxing%20atmosphere%2C%20minimalist%20design&width=800&height=600&seq=1&orientation=landscape",
  description: "프리미엄 마사지 서비스를 제공하는 힐링 스파 센터입니다.",
  phone: "02-1234-5678",
  address: "서울시 강남구 테헤란로 123",
  hours: "09:00 - 22:00",
  featured: true,
  category: "스웨디시",
  gallery: [
    "https://readdy.ai/api/search-image?query=Luxury%20spa%20reception%20area%20with%20modern%20design%2C%20comfortable%20seating%2C%20elegant%20lighting%2C%20professional%20wellness%20center%20entrance&width=600&height=400&seq=2&orientation=landscape",
    "https://readdy.ai/api/search-image?query=Professional%20massage%20therapy%20room%20with%20clean%20white%20linens%2C%20soft%20ambient%20lighting%2C%20essential%20oil%20bottles%2C%20peaceful%20spa%20atmosphere&width=600&height=400&seq=3&orientation=landscape",
    "https://readdy.ai/api/search-image?query=Spa%20relaxation%20lounge%20with%20comfortable%20chairs%2C%20herbal%20tea%20service%2C%20calming%20decor%2C%20wellness%20center%20waiting%20area&width=600&height=400&seq=4&orientation=landscape",
    "https://readdy.ai/api/search-image?query=Modern%20spa%20bathroom%20with%20luxury%20amenities%2C%20clean%20towels%2C%20premium%20toiletries%2C%20elegant%20washroom%20facilities&width=600&height=400&seq=5&orientation=landscape",
    "https://readdy.ai/api/search-image?query=VIP%20massage%20room%20with%20premium%20interior%2C%20luxury%20spa%20bed%2C%20ambient%20lighting%2C%20high-end%20wellness%20facility&width=600&height=400&seq=64&orientation=landscape",
    "https://readdy.ai/api/search-image?query=Couple%20massage%20room%20with%20two%20beds%2C%20romantic%20lighting%2C%20spa%20atmosphere%20for%20couples%20therapy&width=600&height=400&seq=65&orientation=landscape"
  ],
  detailDescription: "힐링 스파 센터는 15년의 경험을 바탕으로 최고 품질의 마사지 서비스를 제공합니다. 숙련된 전문 마사지사들이 개인별 맞춤 케어를 통해 몸과 마음의 완전한 휴식을 선사합니다. 프리미엄 오일과 천연 재료만을 사용하여 안전하고 효과적인 치료를 받으실 수 있습니다. 강남 중심가에 위치하여 접근성이 뛰어나며, 최신 시설과 청결한 환경을 자랑합니다.",
  amenities: ["무료 주차", "샤워시설", "개인 락커", "차/음료 서비스", "WiFi", "에어컨", "음악 서비스", "수건 제공", "로브 제공", "슬리퍼 제공", "헤어드라이어", "어메니티"],
  businessHours: {
    "월요일": "09:00 - 22:00",
    "화요일": "09:00 - 22:00", 
    "수요일": "09:00 - 22:00",
    "목요일": "09:00 - 22:00",
    "금요일": "09:00 - 23:00",
    "토요일": "09:00 - 23:00",
    "일요일": "10:00 - 21:00"
  },
  priceList: [
    {
      service: "스웨디시 마사지",
      duration: "60분",
      price: "80,000원",
      description: "전신 스웨디시 마사지로 근육 이완과 혈액순환 개선"
    },
    {
      service: "스웨디시 마사지",
      duration: "90분",
      price: "110,000원",
      description: "여유로운 90분 코스로 깊은 휴식과 치유"
    },
    {
      service: "아로마 마사지",
      duration: "60분",
      price: "85,000원",
      description: "천연 에센셜 오일을 사용한 향기 치료"
    },
    {
      service: "아로마 마사지",
      duration: "90분",
      price: "120,000원",
      description: "프리미엄 아로마 오일로 몸과 마음의 힐링"
    },
    {
      service: "딥티슈 마사지",
      duration: "60분",
      price: "90,000원",
      description: "깊은 근육층까지 마사지하여 만성 통증 완화"
    },
    {
      service: "커플 마사지",
      duration: "60분",
      price: "160,000원",
      description: "연인, 부부를 위한 특별한 커플 마사지"
    }
  ],
  therapists: [
    {
      id: 1,
      name: "김미영 원장",
      experience: "15년",
      specialty: ["스웨디시", "아로마", "딥티슈"],
      rating: 4.9,
      image: "https://readdy.ai/api/search-image?query=Professional%20female%20massage%20therapist%20in%20white%20uniform%2C%20friendly%20smile%2C%20spa%20clinic%20setting%2C%20Korean%20woman&width=200&height=200&seq=66&orientation=squarish"
    },
    {
      id: 2,
      name: "박지현 실장",
      experience: "12년",
      specialty: ["아로마", "림프마사지", "스포츠마사지"],
      rating: 4.8,
      image: "https://readdy.ai/api/search-image?query=Professional%20female%20massage%20therapist%20in%20spa%20uniform%2C%20confident%20pose%2C%20wellness%20center%20background%2C%20Korean%20woman&width=200&height=200&seq=67&orientation=squarish"
    },
    {
      id: 3,
      name: "이수진 팀장",
      experience: "10년",
      specialty: ["스웨디시", "핫스톤", "커플마사지"],
      rating: 4.7,
      image: "https://readdy.ai/api/search-image?query=Professional%20female%20massage%20therapist%20in%20white%20spa%20attire%2C%20warm%20smile%2C%20luxury%20spa%20interior%2C%20Korean%20woman&width=200&height=200&seq=68&orientation=squarish"
    }
  ],
  policies: [
    "예약 변경은 최소 2시간 전에 연락 바랍니다",
    "노쇼 시 예약금이 환불되지 않습니다",
    "음주 후 서비스 이용이 제한될 수 있습니다",
    "개인 위생용품은 제공되지만 개인 소지품 사용 가능합니다",
    "휴대폰은 매너모드로 설정해 주세요",
    "귀중품은 개인 락커에 보관해 주세요"
  ],
  reviews: [
    {
      id: 1,
      userName: "김**",
      rating: 5,
      comment: "정말 만족스러운 마사지였습니다. 김미영 원장님이 매우 전문적이고 친절하셨어요. 시설도 깨끗하고 분위기가 좋았습니다. 특히 아로마 오일 향이 정말 좋았고, 마사지 후 몸이 한결 가벼워졌어요.",
      date: "2024-01-15",
      service: "스웨디시 90분",
      images: ["https://readdy.ai/api/search-image?query=Clean%20spa%20interior%20after%20massage%20session%2C%20relaxing%20atmosphere%2C%20customer%20satisfaction&width=300&height=200&seq=69&orientation=landscape"]
    },
    {
      id: 2,
      userName: "이**",
      rating: 4,
      comment: "아로마 마사지 받았는데 향이 정말 좋았어요. 스트레스가 많이 풀렸습니다. 다음에도 또 올 예정입니다. 다만 주차공간이 조금 협소한 것 같아요.",
      date: "2024-01-12",
      service: "아로마 60분"
    },
    {
      id: 3,
      userName: "박**",
      rating: 5,
      comment: "딥티슈 마사지로 어깨 결림이 완전히 해결됐어요. 가격 대비 정말 만족스럽습니다. 강력 추천! 박지현 실장님 실력이 정말 좋으세요.",
      date: "2024-01-10",
      service: "딥티슈 60분"
    },
    {
      id: 4,
      userName: "최**",
      rating: 4,
      comment: "시설이 깨끗하고 직원분들이 친절해요. 예약도 편리하고 접근성도 좋습니다. 샤워시설도 깔끔하고 어메니티도 좋았어요.",
      date: "2024-01-08",
      service: "스웨디시 60분"
    },
    {
      id: 5,
      userName: "정**",
      rating: 5,
      comment: "커플 마사지로 남편과 함께 받았는데 정말 좋았어요. 분위기도 로맨틱하고 마사지사분들도 전문적이셨습니다. 기념일에 또 오고 싶어요.",
      date: "2024-01-05",
      service: "커플 마사지 60분",
      images: ["https://readdy.ai/api/search-image?query=Couple%20massage%20room%20with%20romantic%20atmosphere%2C%20two%20massage%20beds%2C%20soft%20lighting&width=300&height=200&seq=70&orientation=landscape"]
    },
    {
      id: 6,
      userName: "한**",
      rating: 4,
      comment: "회사 근처라 자주 이용하는데 항상 만족스러워요. 특히 점심시간에 짧은 코스로 받기 좋습니다. 직장인 할인도 있으면 좋겠어요.",
      date: "2024-01-03",
      service: "스웨디시 60분"
    }
  ]
};

export default function ShopDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  console.log('ShopDetail - ID:', id);
  console.log('ShopDetail - shopsData:', shopsData);

  // 실제 크롤링 데이터에서 해당 ID의 업소 찾기
  const realShop = shopsData.find((s: any) => s.id === parseInt(id || '1'));

  console.log('ShopDetail - realShop:', realShop);

  // 데이터가 없으면 에러 페이지 표시
  if (!realShop && !mockShop) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center text-white">
          <h1 className="text-2xl mb-4">업소를 찾을 수 없습니다</h1>
          <button
            onClick={() => navigate('/')}
            className="bg-pink-600 px-6 py-2 rounded-lg hover:bg-pink-700"
          >
            메인으로 돌아가기
          </button>
        </div>
      </div>
    );
  }

  // 데이터가 없으면 mockShop 사용, gallery가 없으면 빈 배열로 초기화
  const shopData = { ...(realShop || mockShop) };
  if (!shopData.gallery || shopData.gallery.length === 0) {
    shopData.gallery = [shopData.image];
  }
  if (!shopData.reviews || shopData.reviews.length === 0) {
    shopData.reviews = mockShop.reviews || [];
  }
  if (!shopData.amenities || shopData.amenities.length === 0) {
    shopData.amenities = mockShop.amenities || [];
  }
  if (!shopData.priceList || shopData.priceList.length === 0) {
    shopData.priceList = mockShop.priceList || [];
  }
  if (!shopData.businessHours) {
    shopData.businessHours = mockShop.businessHours || {};
  }

  const [shop] = useState<MassageShop>(shopData);

  console.log('ShopDetail - Final shop:', shop);

  const [selectedImage, setSelectedImage] = useState(0);
  const [showReservation, setShowReservation] = useState(false);
  const [isFavorite, setIsFavorite] = useState(false);
  const [showAllReviews, setShowAllReviews] = useState(false);
  const [activeTab, setActiveTab] = useState('info');

  const handleReservation = () => {
    setShowReservation(true);
  };

  const handleCall = () => {
    window.open(`tel:${shop.phone}`);
  };

  const toggleFavorite = () => {
    setIsFavorite(!isFavorite);
  };

  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <i
        key={i}
        className={`ri-star-${i < rating ? 'fill' : 'line'} text-yellow-400 text-sm`}
      />
    ));
  };

  const getCurrentDay = () => {
    const days = ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일'];
    return days[new Date().getDay()];
  };

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 shadow-sm border-b border-gray-700 sticky top-0 z-50">
        <div className="w-full px-3 sm:px-4 lg:px-8">
          <div className="flex justify-between items-center h-14 sm:h-16">
            <div className="flex items-center space-x-3 sm:space-x-4">
              <button
                onClick={() => navigate('/')}
                className="text-gray-300 hover:text-white cursor-pointer"
              >
                <i className="ri-arrow-left-line text-xl"></i>
              </button>
              <h1
                className="text-lg sm:text-xl md:text-2xl font-bold text-pink-400"
                style={{ fontFamily: "Pacifico, serif" }}
              >
                터치앤힐
              </h1>
            </div>

            <div className="flex items-center space-x-2 sm:space-x-3">
              <button
                onClick={toggleFavorite}
                className="p-2 text-gray-300 hover:text-pink-400 cursor-pointer"
              >
                <i className={`ri-heart-${isFavorite ? 'fill' : 'line'} text-xl`}></i>
              </button>
              <button className="p-2 text-gray-300 hover:text-white cursor-pointer">
                <i className="ri-share-line text-xl"></i>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* 원본 팝업 페이지 iframe으로 표시 */}
      {shop.url && (
        <section className="bg-gray-800">
          <div className="w-full px-3 sm:px-4 lg:px-8 py-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-white text-base font-semibold">원본 업소 상세 정보</h3>
              <a
                href={shop.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-pink-400 text-sm hover:text-pink-300 flex items-center gap-1"
              >
                새 창에서 열기 <i className="ri-external-link-line"></i>
              </a>
            </div>
            <div className="bg-gray-900 rounded-lg overflow-hidden" style={{ height: '600px' }}>
              <iframe
                src={shop.url}
                className="w-full h-full border-0"
                title={shop.name}
                sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
              />
            </div>
          </div>
        </section>
      )}

      {/* Image Gallery */}
      <section className="bg-gray-800">
        <div className="w-full">
          {/* Thumbnail Gallery - 크롤링된 상세 이미지 표시 */}
          {shop.gallery && shop.gallery.length > 0 && (
            <div className="p-3 sm:p-4">
              <h3 className="text-white text-base font-semibold mb-3">
                상세 이미지 갤러리 ({shop.gallery.length}개)
              </h3>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-2 sm:gap-3">
                {shop.gallery.map((image, index) => (
                  <div
                    key={index}
                    className="relative aspect-square rounded-lg overflow-hidden border border-gray-600 hover:border-pink-500 transition-all cursor-pointer"
                    onClick={() => window.open(image, '_blank')}
                  >
                    <img
                      src={image}
                      alt={`Gallery ${index + 1}`}
                      className="w-full h-full object-cover hover:scale-110 transition-transform duration-300"
                      onError={(e) => {
                        (e.target as HTMLImageElement).src = shop.image;
                      }}
                    />
                    <div className="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 transition-all flex items-center justify-center">
                      <i className="ri-zoom-in-line text-white text-2xl opacity-0 hover:opacity-100"></i>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Shop Info */}
      <section className="bg-gray-800 border-b border-gray-700">
        <div className="w-full px-3 sm:px-4 lg:px-8 py-4 sm:py-6">
          <div className="flex justify-between items-start mb-3 sm:mb-4">
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-2">
                <h1 className="text-xl sm:text-2xl lg:text-3xl font-bold text-white">
                  {shop.name}
                </h1>
                {shop.featured && (
                  <span className="bg-pink-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                    추천
                  </span>
                )}
              </div>
              
              <div className="flex items-center space-x-4 mb-2">
                <div className="flex items-center">
                  {renderStars(Math.floor(shop.rating))}
                  <span className="text-white font-semibold ml-2">{shop.rating}</span>
                  <span className="text-gray-400 ml-1">({shop.reviews.length}개 리뷰)</span>
                </div>
              </div>

              <div className="flex items-center text-gray-400 mb-2">
                <i className="ri-map-pin-line text-sm mr-2"></i>
                <span className="text-sm">{shop.address}</span>
              </div>

              <div className="flex items-center text-gray-400 mb-2">
                <i className="ri-time-line text-sm mr-2"></i>
                <span className="text-sm">{shop.businessHours[getCurrentDay()]}</span>
                <span className="text-green-400 ml-2 text-xs">영업중</span>
              </div>

              <div className="flex items-center text-gray-400 mb-3">
                <i className="ri-phone-line text-sm mr-2"></i>
                <span className="text-sm">{shop.phone}</span>
              </div>

              <div className="flex flex-wrap gap-2">
                {shop.services.map(service => (
                  <span
                    key={service}
                    className="bg-gray-600 text-gray-300 px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm"
                  >
                    {service}
                  </span>
                ))}
              </div>
            </div>

            <div className="text-right ml-4">
              <div className="text-xl sm:text-2xl font-bold text-pink-400 mb-2">
                {shop.price}
              </div>
              <span className="bg-gray-600 text-gray-300 px-2 py-1 rounded text-xs">
                {shop.category}
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Action Buttons */}
      <section className="bg-gray-800 border-b border-gray-700">
        <div className="w-full px-3 sm:px-4 lg:px-8 py-3 sm:py-4">
          <div className="flex space-x-2 sm:space-x-3">
            <button
              onClick={handleCall}
              className="flex-1 bg-gray-600 text-white py-3 rounded-lg hover:bg-gray-500 cursor-pointer flex items-center justify-center space-x-2"
            >
              <i className="ri-phone-line"></i>
              <span className="text-sm sm:text-base">전화하기</span>
            </button>
            <button
              onClick={handleReservation}
              className="flex-1 bg-pink-600 text-white py-3 rounded-lg hover:bg-pink-700 cursor-pointer flex items-center justify-center space-x-2"
            >
              <i className="ri-calendar-line"></i>
              <span className="text-sm sm:text-base">예약하기</span>
            </button>
          </div>
        </div>
      </section>

      {/* Tab Navigation */}
      <section className="bg-gray-800 border-b border-gray-700">
        <div className="w-full px-3 sm:px-4 lg:px-8">
          <div className="flex space-x-1">
            {[
              { id: 'info', label: '업소정보', icon: 'ri-information-line' },
              { id: 'price', label: '가격표', icon: 'ri-price-tag-3-line' },
              { id: 'therapist', label: '마사지사', icon: 'ri-user-heart-line' },
              { id: 'review', label: '리뷰', icon: 'ri-star-line' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 py-3 px-2 text-center border-b-2 transition-colors cursor-pointer ${
                  activeTab === tab.id
                    ? 'border-pink-500 text-pink-400'
                    : 'border-transparent text-gray-400 hover:text-gray-300'
                }`}
              >
                <i className={`${tab.icon} text-sm mr-1`}></i>
                <span className="text-xs sm:text-sm font-medium">{tab.label}</span>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Tab Content */}
      <section className="bg-gray-900 py-4 sm:py-6">
        <div className="w-full px-3 sm:px-4 lg:px-8">
          {/* Info Tab */}
          {activeTab === 'info' && (
            <div className="space-y-6">
              {/* Description */}
              <div>
                <h3 className="text-lg sm:text-xl font-bold text-white mb-3 sm:mb-4">업소 소개</h3>
                <p className="text-gray-300 text-sm sm:text-base leading-relaxed">
                  {shop.detailDescription}
                </p>
              </div>

              {/* Business Hours */}
              <div>
                <h3 className="text-lg sm:text-xl font-bold text-white mb-3 sm:mb-4">운영시간</h3>
                <div className="bg-gray-800 rounded-lg p-4">
                  {Object.entries(shop.businessHours).map(([day, hours]) => (
                    <div key={day} className={`flex justify-between items-center py-2 ${
                      day === getCurrentDay() ? 'text-pink-400 font-semibold' : 'text-gray-300'
                    }`}>
                      <span className="text-sm">{day}</span>
                      <span className="text-sm">{hours}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Amenities */}
              <div>
                <h3 className="text-lg sm:text-xl font-bold text-white mb-3 sm:mb-4">편의시설</h3>
                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2 sm:gap-3">
                  {shop.amenities.map(amenity => (
                    <div
                      key={amenity}
                      className="flex items-center space-x-2 bg-gray-800 p-2 sm:p-3 rounded-lg"
                    >
                      <i className="ri-check-line text-green-400 text-sm"></i>
                      <span className="text-gray-300 text-xs sm:text-sm">{amenity}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Policies */}
              <div>
                <h3 className="text-lg sm:text-xl font-bold text-white mb-3 sm:mb-4">이용안내</h3>
                <div className="bg-gray-800 rounded-lg p-4">
                  {shop.policies.map((policy, index) => (
                    <div key={index} className="flex items-start space-x-2 py-2">
                      <i className="ri-information-line text-pink-400 text-sm mt-0.5"></i>
                      <span className="text-gray-300 text-sm">{policy}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Map */}
              <div>
                <h3 className="text-lg sm:text-xl font-bold text-white mb-3 sm:mb-4">위치</h3>
                <div className="bg-gray-700 rounded-lg overflow-hidden">
                  <iframe
                    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3165.4!2d127.0276!3d37.4979!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMzfCsDI5JzUyLjQiTiAxMjfCsDAxJzM5LjQiRQ!5e0!3m2!1sen!2skr!4v1234567890"
                    width="100%"
                    height="200"
                    style={{ border: 0 }}
                    allowFullScreen
                    loading="lazy"
                    referrerPolicy="no-referrer-when-downgrade"
                  ></iframe>
                </div>
                <div className="mt-3 p-3 bg-gray-800 rounded-lg">
                  <div className="flex items-center space-x-2 text-gray-300">
                    <i className="ri-map-pin-line text-pink-400"></i>
                    <span className="text-sm">{shop.address}</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Price Tab */}
          {activeTab === 'price' && (
            <div>
              <h3 className="text-lg sm:text-xl font-bold text-white mb-4">가격표</h3>
              <div className="space-y-3">
                {shop.priceList.map((item, index) => (
                  <div key={index} className="bg-gray-800 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h4 className="text-white font-semibold text-sm sm:text-base">{item.service}</h4>
                        <p className="text-gray-400 text-xs sm:text-sm">{item.duration}</p>
                      </div>
                      <span className="text-pink-400 font-bold text-lg">{item.price}</span>
                    </div>
                    <p className="text-gray-300 text-xs sm:text-sm">{item.description}</p>
                  </div>
                ))}
              </div>
              <div className="mt-4 p-3 bg-gray-800 rounded-lg">
                <p className="text-gray-400 text-xs">
                  * 가격은 변동될 수 있으며, 정확한 가격은 전화 문의 바랍니다.
                </p>
              </div>
            </div>
          )}

          {/* Therapist Tab */}
          {activeTab === 'therapist' && (
            <div>
              <h3 className="text-lg sm:text-xl font-bold text-white mb-4">마사지사 소개</h3>
              <div className="space-y-4">
                {shop.therapists.map(therapist => (
                  <div key={therapist.id} className="bg-gray-800 rounded-lg p-4">
                    <div className="flex items-start space-x-4">
                      <img
                        src={therapist.image}
                        alt={therapist.name}
                        className="w-16 h-16 sm:w-20 sm:h-20 rounded-full object-cover"
                      />
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <h4 className="text-white font-semibold text-sm sm:text-base">{therapist.name}</h4>
                          <div className="flex items-center">
                            {renderStars(Math.floor(therapist.rating))}
                            <span className="text-gray-400 text-xs ml-1">{therapist.rating}</span>
                          </div>
                        </div>
                        <p className="text-gray-400 text-xs sm:text-sm mb-2">경력 {therapist.experience}</p>
                        <div className="flex flex-wrap gap-1">
                          {therapist.specialty.map(spec => (
                            <span
                              key={spec}
                              className="bg-gray-600 text-gray-300 px-2 py-1 rounded text-xs"
                            >
                              {spec}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Review Tab */}
          {activeTab === 'review' && (
            <div>
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg sm:text-xl font-bold text-white">
                  리뷰 ({shop.reviews.length})
                </h3>
                <button className="text-pink-400 hover:text-pink-300 text-sm cursor-pointer">
                  리뷰 작성하기
                </button>
              </div>

              <div className="space-y-4">
                {(showAllReviews ? shop.reviews : shop.reviews.slice(0, 3)).map(review => (
                  <div key={review.id} className="bg-gray-800 p-4 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex items-center space-x-2">
                        <span className="text-white font-medium text-sm">{review.userName}</span>
                        <span className="bg-gray-600 text-gray-300 px-2 py-1 rounded text-xs">
                          {review.service}
                        </span>
                      </div>
                      <span className="text-gray-400 text-xs">{review.date}</span>
                    </div>
                    
                    <div className="flex items-center mb-2">
                      {renderStars(review.rating)}
                    </div>
                    
                    <p className="text-gray-300 text-sm leading-relaxed mb-3">
                      {review.comment}
                    </p>

                    {review.images && (
                      <div className="flex space-x-2">
                        {review.images.map((image, index) => (
                          <img
                            key={index}
                            src={image}
                            alt={`Review ${index + 1}`}
                            className="w-16 h-16 sm:w-20 sm:h-20 rounded-lg object-cover cursor-pointer"
                          />
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {shop.reviews.length > 3 && (
                <div className="text-center mt-4">
                  <button
                    onClick={() => setShowAllReviews(!showAllReviews)}
                    className="text-pink-400 hover:text-pink-300 text-sm cursor-pointer"
                  >
                    {showAllReviews ? '접기' : `더보기 (${shop.reviews.length - 3}개 더)`}
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </section>

      {/* Reservation Modal */}
      {showReservation && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 rounded-lg w-full max-w-md">
            <div className="flex justify-between items-center p-4 border-b border-gray-700">
              <h3 className="text-lg font-bold text-white">예약하기</h3>
              <button
                onClick={() => setShowReservation(false)}
                className="text-gray-400 hover:text-white cursor-pointer"
              >
                <i className="ri-close-line text-xl"></i>
              </button>
            </div>
            
            <div className="p-4">
              <div className="text-center py-8">
                <i className="ri-calendar-check-line text-4xl text-pink-400 mb-4"></i>
                <h4 className="text-lg font-medium text-white mb-2">예약 시스템</h4>
                <p className="text-gray-400 text-sm mb-6">
                  예약 기능은 다음 단계에서 구현됩니다.
                </p>
                <button
                  onClick={handleCall}
                  className="bg-pink-600 text-white px-6 py-3 rounded-lg hover:bg-pink-700 cursor-pointer"
                >
                  전화로 예약하기
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Bottom Navigation */}
      <div className="sticky bottom-0 bg-gray-800 border-t border-gray-700 p-3 sm:p-4">
        <div className="flex space-x-2 sm:space-x-3">
          <button
            onClick={handleCall}
            className="flex-1 bg-gray-600 text-white py-3 rounded-lg hover:bg-gray-500 cursor-pointer flex items-center justify-center space-x-2"
          >
            <i className="ri-phone-line"></i>
            <span className="text-sm sm:text-base">전화</span>
          </button>
          <button
            onClick={handleReservation}
            className="flex-2 bg-pink-600 text-white py-3 rounded-lg hover:bg-pink-700 cursor-pointer flex items-center justify-center space-x-2"
          >
            <i className="ri-calendar-line"></i>
            <span className="text-sm sm:text-base">예약하기</span>
          </button>
        </div>
      </div>
    </div>
  );
}

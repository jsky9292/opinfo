
import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import shopsData from '../../data/shops_data.json';
import { authAPI } from '../../lib/api';

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
  gallery?: string[];
  kakao_id?: string;
  telegram_id?: string;
  url?: string;
}

// 실제 크롤링된 데이터 기준 카테고리 (522개 업체 - 서울 25개 구 전체 포함)
const regions = ["전체", "서울/강남", "대전/충청", "대구/경북", "인천/경기", "부산/경남", "광주/전라", "강원/제주"];
const serviceTypes = ["전체보기", "건마", "휴게텔", "오피스텔", "안마", "룸/풀사롱", "키스방", "기타"];

// 크롤링된 실제 데이터 사용
const mockShops: MassageShop[] = shopsData as MassageShop[];

// 백업용 mockShops data (사용 안 함)
const mockShopsBackup: MassageShop[] = [
  // 서울 지역
  {
    id: 1,
    name: "힐링 스파 센터",
    location: "서울",
    district: "강남구",
    rating: 4.8,
    price: "80,000원~",
    services: ["스웨디시", "아로마", "딥티슈"],
    image:
      "https://readdy.ai/api/search-image?query=Modern%20luxury%20spa%20interior%20with%20massage%20tables%2C%20soft%20lighting%2C%20clean%20white%20and%20beige%20colors%2C%20professional%20massage%20therapy%20room%20with%20relaxing%20atmosphere%2C%20minimalist%20design&width=400&height=300&seq=1&orientation=landscape",
    description: "프리미엄 마사지 서비스를 제공하는 힐링 스파 센터입니다.",
    phone: "02-1234-5678",
    address: "서울시 강남구 테헤란로 123",
    hours: "09:00 - 22:00",
    featured: true,
    category: "스웨디시"
  },
  {
    id: 2,
    name: "릴렉스 마사지",
    location: "서울",
    district: "마포구",
    rating: 4.6,
    price: "60,000원~",
    services: ["타이마사지", "족욕", "전신마사지"],
    image:
      "https://readdy.ai/api/search-image?query=Traditional%20Thai%20massage%20spa%20room%20with%20wooden%20elements%2C%20warm%20lighting%2C%20bamboo%20decorations%2C%20peaceful%20zen%20atmosphere%2C%20professional%20massage%20therapy%20setting&width=400&height=300&seq=2&orientation=landscape",
    description: "전통 타이마사지 전문점으로 숙련된 마사지사가 서비스합니다.",
    phone: "02-2345-6789",
    address: "서울시 마포구 홍익로 456",
    hours: "10:00 - 24:00",
    featured: false,
    category: "타이마사지"
  },
  {
    id: 3,
    name: "웰니스 케어",
    location: "서울",
    district: "송파구",
    rating: 4.7,
    price: "70,000원~",
    services: ["스포츠마사지", "재활마사지", "림프마사지"],
    image:
      "https://readdy.ai/api/search-image?query=Modern%20wellness%20center%20with%20sports%20massage%20equipment%2C%20bright%20clean%20interior%2C%20professional%20therapy%20room%2C%20medical%20grade%20massage%20tables%2C%20contemporary%20design&width=400&height=300&seq=3&orientation=landscape",
    description: "스포츠 마사지와 재활 마사지 전문 웰니스 센터입니다.",
    phone: "02-3456-7890",
    address: "서울시 송파구 잠실로 789",
    hours: "08:00 - 21:00",
    featured: true,
    category: "건마"
  },
  {
    id: 4,
    name: "강남 프리미엄 스파",
    location: "서울",
    district: "강남구",
    rating: 4.9,
    price: "120,000원~",
    services: ["VIP마사지", "커플마사지", "아로마"],
    image:
      "https://readdy.ai/api/search-image?query=Luxury%20premium%20spa%20with%20elegant%20interior%2C%20VIP%20massage%20rooms%2C%20high-end%20wellness%20facility%2C%20sophisticated%20atmosphere&width=400&height=300&seq=39&orientation=landscape",
    description: "강남 최고급 프리미엄 스파로 VIP 서비스를 제공합니다.",
    phone: "02-4567-8901",
    address: "서울시 강남구 논현로 234",
    hours: "10:00 - 23:00",
    featured: true,
    category: "스웨디시"
  },
  {
    id: 5,
    name: "홍대 청춘 마사지",
    location: "서울",
    district: "마포구",
    rating: 4.5,
    price: "45,000원~",
    services: ["학생할인", "타이마사지", "전신마사지"],
    image:
      "https://readdy.ai/api/search-image?query=Youth-friendly%20massage%20center%20with%20modern%20colorful%20interior%2C%20affordable%20wellness%20service%2C%20student-oriented%20spa%20facility&width=400&height=300&seq=40&orientation=landscape",
    description: "홍대 젊은이들을 위한 합리적인 가격의 마사지 전문점입니다.",
    phone: "02-5678-9012",
    address: "서울시 마포구 와우산로 345",
    hours: "12:00 - 02:00",
    featured: false,
    category: "타이마사지"
  },
  {
    id: 6,
    name: "명동 관광객 스파",
    location: "서울",
    district: "중구",
    rating: 4.4,
    price: "65,000원~",
    services: ["외국어서비스", "관광객특가", "스웨디시"],
    image:
      "https://readdy.ai/api/search-image?query=Tourist-friendly%20spa%20in%20downtown%20area%20with%20multilingual%20service%2C%20international%20standard%20massage%20facility%2C%20welcoming%20atmosphere&width=400&height=300&seq=41&orientation=landscape",
    description: "명동 관광객을 위한 다국어 서비스 제공 스파입니다.",
    phone: "02-6789-0123",
    address: "서울시 중구 명동길 456",
    hours: "09:00 - 22:00",
    featured: false,
    category: "스웨디시"
  },
  {
    id: 7,
    name: "종로 전통 마사지",
    location: "서울",
    district: "종로구",
    rating: 4.3,
    price: "55,000원~",
    services: ["한방마사지", "경락마사지", "추나요법"],
    image:
      "https://readdy.ai/api/search-image?query=Traditional%20Korean%20medicine%20spa%20with%20herbal%20elements%2C%20wooden%20interior%2C%20oriental%20massage%20room%2C%20traditional%20healing%20atmosphere%2C%20natural%20materials&width=400&height=300&seq=60&orientation=landscape",
    description: "종로의 전통 한방 마사지를 경험하실 수 있습니다.",
    phone: "02-7890-1234",
    address: "서울시 종로구 종로 567",
    hours: "09:00 - 21:00",
    featured: false,
    category: "한방마사지"
  },

  // 부산 지역
  {
    id: 8,
    name: "부산 오션 스파",
    location: "부산",
    district: "해운대구",
    rating: 4.9,
    price: "75,000원~",
    services: ["아로마마사지", "핫스톤", "바다소금마사지"],
    image:
      "https://readdy.ai/api/search-image?query=Ocean%20view%20spa%20with%20sea%20salt%20therapy%2C%20coastal%20massage%20room%20with%20blue%20and%20white%20colors%2C%20relaxing%20beach%20atmosphere%2C%20professional%20spa%20interior&width=400&height=300&seq=22&orientation=landscape",
    description: "바다 전망과 함께하는 특별한 스파 경험을 제공합니다.",
    phone: "051-1234-5678",
    address: "부산시 해운대구 해운대해변로 100",
    hours: "09:00 - 23:00",
    featured: true,
    category: "아로마"
  },
  {
    id: 9,
    name: "해운대 비치 마사지",
    location: "부산",
    district: "해운대구",
    rating: 4.6,
    price: "68,000원~",
    services: ["비치테라피", "선탠케어", "스웨디시"],
    image:
      "https://readdy.ai/api/search-image?query=Beachside%20massage%20center%20with%20ocean%20breeze%2C%20coastal%20therapy%20room%2C%20summer%20vacation%20spa%20atmosphere&width=400&height=300&seq=42&orientation=landscape",
    description: "해운대 해변가에서 즐기는 특별한 비치 테라피입니다.",
    phone: "051-2345-6789",
    address: "부산시 해운대구 구남로 200",
    hours: "08:00 - 22:00",
    featured: false,
    category: "스웨디시"
  },
  {
    id: 10,
    name: "광안리 야경 스파",
    location: "부산",
    district: "수영구",
    rating: 4.7,
    price: "82,000원~",
    services: ["야경마사지", "커플스파", "아로마"],
    image:
      "https://readdy.ai/api/search-image?query=Night%20view%20spa%20with%20city%20lights%2C%20romantic%20couple%20massage%20room%2C%20evening%20wellness%20atmosphere%2C%20luxury%20coastal%20spa&width=400&height=300&seq=43&orientation=landscape",
    description: "광안리 야경을 감상하며 받는 로맨틱한 커플 스파입니다.",
    phone: "051-3456-7890",
    address: "부산시 수영구 광안해변로 300",
    hours: "14:00 - 24:00",
    featured: true,
    category: "아로마"
  },
  {
    id: 11,
    name: "서면 24시 마사지",
    location: "부산",
    district: "부산진구",
    rating: 4.4,
    price: "58,000원~",
    services: ["24시간", "전신마사지", "타이마사지"],
    image:
      "https://readdy.ai/api/search-image?query=24-hour%20massage%20center%20with%20comfortable%20interior%2C%20night%20service%20massage%20facility%2C%20urban%20wellness%20center&width=400&height=300&seq=61&orientation=landscape",
    description: "부산 서면의 24시간 운영 마사지 전문점입니다.",
    phone: "051-4567-8901",
    address: "부산시 부산진구 서면로 400",
    hours: "24시간",
    featured: false,
    category: "타이마사지"
  },

  // 대전 지역
  {
    id: 12,
    name: "대전 과학도시 웰니스",
    location: "대전",
    district: "유성구",
    rating: 4.7,
    price: "72,000원~",
    services: ["스포츠마사지", "근막이완", "재활치료"],
    image:
      "https://readdy.ai/api/search-image?query=High-tech%20wellness%20center%20with%20modern%20equipment%2C%20scientific%20approach%20massage%20therapy%2C%20clean%20white%20interior%2C%20professional%20sports%20medicine%20facility&width=400&height=300&seq=26&orientation=landscape",
    description: "과학적 접근법을 통한 전문 스포츠 마사지 센터입니다.",
    phone: "042-5678-9012",
    address: "대전시 유성구 대학로 500",
    hours: "08:00 - 21:00",
    featured: true,
    category: "건마"
  },
  {
    id: 13,
    name: "유성온천 힐링스파",
    location: "대전",
    district: "유성구",
    rating: 4.9,
    price: "95,000원~",
    services: ["온천마사지", "스파테라피", "커플스파"],
    image:
      "https://readdy.ai/api/search-image?query=Hot%20spring%20spa%20resort%20with%20natural%20mineral%20water%2C%20luxury%20wellness%20facility%2C%20traditional%20Korean%20spa%20atmosphere%2C%20healing%20hot%20springs&width=400&height=300&seq=47&orientation=landscape",
    description: "유성온천의 천연 미네랄을 활용한 프리미엄 스파입니다.",
    phone: "042-7890-1234",
    address: "대전시 유성구 온천로 700",
    hours: "06:00 - 24:00",
    featured: true,
    category: "스웨디시"
  },
  {
    id: 14,
    name: "중구 전통 마사지",
    location: "대전",
    district: "중구",
    rating: 4.5,
    price: "62,000원~",
    services: ["한방마사지", "경락마사지", "추나요법"],
    image:
      "https://readdy.ai/api/search-image?query=Traditional%20Korean%20medicine%20clinic%20with%20herbal%20medicine%20cabinets%2C%20wooden%20furniture%2C%20oriental%20healing%20atmosphere%2C%20professional%20traditional%20therapy%20room&width=400&height=300&seq=62&orientation=landscape",
    description: "대전 중구의 전통 한방 마사지 전문점입니다.",
    phone: "042-8901-2345",
    address: "대전시 중구 대종로 800",
    hours: "09:00 - 20:00",
    featured: false,
    category: "한방마사지"
  },
  {
    id: 15,
    name: "서구 힐링센터",
    location: "대전",
    district: "서구",
    rating: 4.6,
    price: "68,000원~",
    services: ["아로마", "스웨디시", "림프마사지"],
    image:
      "https://readdy.ai/api/search-image?query=Modern%20healing%20center%20with%20aromatherapy%2C%20relaxing%20spa%20interior%2C%20professional%20massage%20facility%2C%20peaceful%20wellness%20atmosphere&width=400&height=300&seq=63&orientation=landscape",
    description: "대전 서구의 현대적인 힐링 센터입니다.",
    phone: "042-9012-3456",
    address: "대전시 서구 둔산로 900",
    hours: "10:00 - 22:00",
    featured: false,
    category: "아로마"
  },

  // 기타 지역들도 동일하게 district 추가...
  {
    id: 16,
    name: "인천공항 스파",
    location: "인천",
    district: "중구",
    rating: 4.5,
    price: "85,000원~",
    services: ["스웨디시", "비즈니스마사지", "피로회복"],
    image:
      "https://readdy.ai/api/search-image?query=Modern%20airport%20spa%20with%20comfortable%20massage%20chairs%2C%20business%20traveler%20friendly%20interior%2C%20professional%20quick%20massage%20service%2C%20contemporary%20design&width=400&height=300&seq=24&orientation=landscape",
    description: "여행 피로를 풀어주는 공항 근처 전문 스파입니다.",
    phone: "032-3456-7890",
    address: "인천시 중구 공항로 300",
    hours: "06:00 - 24:00",
    featured: false,
    category: "스웨디시"
  },
  {
    id: 17,
    name: "송도 국제 웰니스",
    location: "인천",
    district: "연수구",
    rating: 4.7,
    price: "78,000원~",
    services: ["국제표준마사지", "비즈니스스파", "스웨디시"],
    image:
      "https://readdy.ai/api/search-image?query=International%20business%20district%20spa%20with%20modern%20architecture%2C%20professional%20wellness%20center%2C%20high-tech%20massage%20facility%2C%20corporate%20atmosphere&width=400&height=300&seq=45&orientation=landscape",
    description: "송도 국제업무단지의 글로벌 스탠다드 웰니스 센터입니다.",
    phone: "032-5678-9012",
    address: "인천시 연수구 송도과학로 500",
    hours: "07:00 - 23:00",
    featured: true,
    category: "스웨디시"
  }
];

// Region and district mapping - 실제 크롤링된 전국 데이터 기준 (522개 업체)
const regionDistricts: { [key: string]: string[] } = {
  "전체": [],
  "서울/강남": ["전체", "강남", "관악", "송파", "강동", "도봉", "동대문", "마포", "영등포"],
  "대전/충청": ["전체", "대전", "천안", "청주", "세종", "아산", "오창", "당진", "진천", "충주", "서산", "보령", "홍성", "논산", "오송", "음성"],
  "대구/경북": ["전체", "대구", "구미"],
  "인천/경기": ["전체", "인천", "수원", "용인"],
  "부산/경남": ["전체", "부산"],
  "광주/전라": ["전체", "광주", "전주", "군산", "익산"],
  "강원/제주": ["전체", "제주"]
};

export default function Home() {
  const navigate = useNavigate();
  const [selectedRegion, setSelectedRegion] = useState("전체");
  const [selectedCity, setSelectedCity] = useState("전체"); // 서브 도시 선택
  const [selectedServiceType, setSelectedServiceType] = useState("전체보기");
  const [searchTerm, setSearchTerm] = useState("");
  const [showMobileMenu, setShowMobileMenu] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await authAPI.getMe();
      if (response.success && response.data?.user) {
        setUser(response.data.user);
        setIsLoggedIn(true);
      }
    } catch (error) {
      setIsLoggedIn(false);
      setUser(null);
    }
  };

  const handleLogout = () => {
    authAPI.logout();
    setIsLoggedIn(false);
    setUser(null);
    alert('로그아웃되었습니다.');
  };

  const filteredShops = mockShops.filter(shop => {
    // 1단계: 지역 필터 (서울/강남, 대전/충청, 대구/경북 등)
    let matchesRegion = selectedRegion === "전체";
    if (!matchesRegion) {
      // 실제 크롤링된 데이터 기준 매핑
      if (selectedRegion === "서울/강남") {
        matchesRegion = shop.location === "서울";
      }
      else if (selectedRegion === "대전/충청") {
        matchesRegion = shop.location === "대전";
      }
      else if (selectedRegion === "대구/경북") {
        matchesRegion = shop.location === "대구";
      }
      else if (selectedRegion === "인천/경기") {
        matchesRegion = shop.location === "경기";
      }
      else if (selectedRegion === "부산/경남") {
        matchesRegion = shop.location === "부산";
      }
      else if (selectedRegion === "광주/전라") {
        matchesRegion = shop.location === "광주";
      }
      else if (selectedRegion === "강원/제주") {
        matchesRegion = shop.location === "강원";
      }
    }

    // 2단계: 서브 도시 필터 (대전, 천안, 청주 등)
    let matchesCity = true;
    if (selectedRegion !== "전체" && selectedCity !== "전체") {
      // district 필드에서 도시명 포함 여부 체크
      matchesCity = shop.district.includes(selectedCity);
    }

    // 3단계: 업종 필터 (건마, 휴게텔, 오피스텔 등)
    const matchesServiceType =
      selectedServiceType === "전체보기" || shop.category === selectedServiceType;

    // 4단계: 검색어 필터
    const matchesSearch =
      searchTerm === "" ||
      shop.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      shop.location.toLowerCase().includes(searchTerm.toLowerCase()) ||
      shop.district.toLowerCase().includes(searchTerm.toLowerCase());

    return matchesRegion && matchesCity && matchesServiceType && matchesSearch;
  });

  const featuredShops = filteredShops.filter(shop => shop.featured);

  const handleShopClick = (shopId: number) => {
    navigate(`/shop/${shopId}`);
  };

  const handleRegionChange = (region: string) => {
    setSelectedRegion(region);
    setSelectedDistrict("전체"); // Reset district when region changes
  };

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 shadow-sm border-b border-gray-700 sticky top-0 z-50">
        <div className="w-full px-3 sm:px-4 lg:px-8">
          <div className="flex justify-between items-center h-14 sm:h-16">
            <div className="flex items-center">
              <h1
                className="text-lg sm:text-xl md:text-2xl font-bold text-pink-400"
                style={{ fontFamily: "Pacifico, serif" }}
              >
                오피인포
              </h1>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden lg:flex space-x-6 xl:space-x-8">
              <a
                href="#"
                className="text-gray-300 hover:text-pink-400 font-medium text-sm xl:text-base"
              >
                홈
              </a>
              <a
                href="#"
                className="text-gray-300 hover:text-pink-400 font-medium text-sm xl:text-base"
              >
                업소 찾기
              </a>
              <a
                href="#"
                className="text-gray-300 hover:text-pink-400 font-medium text-sm xl:text-base"
              >
                리뷰
              </a>
              <a
                href="#"
                className="text-gray-300 hover:text-pink-400 font-medium text-sm xl:text-base"
              >
                이벤트
              </a>
              <a
                href="#"
                className="text-gray-300 hover:text-pink-400 font-medium text-sm xl:text-base"
              >
                고객센터
              </a>
            </nav>

            <div className="flex items-center space-x-2 sm:space-x-4">
              {/* 포인트 표시 */}
              <div className="hidden md:flex items-center bg-gray-700 px-3 py-2 rounded-lg">
                <i className="ri-coin-line text-yellow-400 mr-2"></i>
                <span className="text-white text-sm font-medium">100P</span>
              </div>

              {/* 로그인/회원가입 */}
              <div className="hidden sm:flex items-center space-x-2">
                {isLoggedIn && user ? (
                  <>
                    <span className="text-gray-300 text-sm">{user.username}님</span>
                    {user.isAdmin && (
                      <Link
                        to="/admin/dashboard"
                        className="text-pink-400 hover:text-pink-300 px-3 py-2 text-sm"
                      >
                        관리자
                      </Link>
                    )}
                    <button
                      onClick={handleLogout}
                      className="text-gray-300 hover:text-white px-3 py-2 text-sm"
                    >
                      로그아웃
                    </button>
                  </>
                ) : (
                  <>
                    <Link
                      to="/auth/login"
                      className="text-gray-300 hover:text-white px-3 py-2 text-sm"
                    >
                      로그인
                    </Link>
                    <Link
                      to="/auth/signup"
                      className="bg-pink-600 text-white px-3 md:px-4 py-2 rounded-lg hover:bg-pink-700 whitespace-nowrap text-xs md:text-sm"
                    >
                      회원가입
                    </Link>
                  </>
                )}
              </div>

              {/* Mobile Menu Button */}
              <button
                className="lg:hidden p-2 text-gray-300 hover:text-white cursor-pointer"
                onClick={() => setShowMobileMenu(!showMobileMenu)}
              >
                <i
                  className={`ri-${showMobileMenu ? "close" : "menu"}-line text-xl`}
                ></i>
              </button>
            </div>
          </div>

          {/* Mobile Menu */}
          {showMobileMenu && (
            <div className="lg:hidden border-t border-gray-700 bg-gray-800 py-3">
              <nav className="flex flex-col space-y-2">
                <a
                  href="#"
                  className="text-gray-300 hover:text-pink-400 font-medium px-2 py-2 text-sm"
                >
                  홈
                </a>
                <a
                  href="#"
                  className="text-gray-300 hover:text-pink-400 font-medium px-2 py-2 text-sm"
                >
                  업소 찾기
                </a>
                <a
                  href="#"
                  className="text-gray-300 hover:text-pink-400 font-medium px-2 py-2 text-sm"
                >
                  리뷰
                </a>
                <a
                  href="#"
                  className="text-gray-300 hover:text-pink-400 font-medium px-2 py-2 text-sm"
                >
                  이벤트
                </a>
                <a
                  href="#"
                  className="text-gray-300 hover:text-pink-400 font-medium px-2 py-2 text-sm"
                >
                  고객센터
                </a>
                <button className="sm:hidden bg-pink-600 text-white px-4 py-2 rounded-lg hover:bg-pink-700 whitespace-nowrap cursor-pointer text-sm mx-2 mt-2">
                  업소 등록
                </button>
              </nav>
            </div>
          )}
        </div>
      </header>

      {/* Hero Section */}
      <section
        className="relative bg-gradient-to-r from-gray-800 to-gray-900 text-white py-8 sm:py-12 md:py-16 lg:py-20"
        style={{
          backgroundImage:
            "url('https://readdy.ai/api/search-image?query=Dark%20elegant%20spa%20wellness%20center%20with%20purple%20and%20pink%20neon%20lighting%2C%20modern%20luxury%20massage%20therapy%20interior%2C%20sophisticated%20night%20atmosphere%2C%20professional%20spa%20setting&width=1200&height=600&seq=7&orientation=landscape')",
          backgroundSize: "cover",
          backgroundPosition: "center"
        }}
      >
        <div className="absolute inset-0 bg-black/60"></div>
        <div className="relative w-full px-3 sm:px-4 lg:px-8 text-center">
          <h2 className="text-xl sm:text-2xl md:text-3xl lg:text-4xl xl:text-5xl font-bold mb-3 sm:mb-4 md:mb-6 leading-tight px-2">
            <span className="block sm:inline">전국 최고의 마사지 업소를</span>
            <span className="block sm:inline sm:ml-2">한 곳에서 찾아보세요</span>
          </h2>
          <p className="text-sm sm:text-base md:text-lg lg:text-xl xl:text-2xl mb-4 sm:mb-6 md:mb-8 opacity-90 px-2 sm:px-4">
            검증된 업소만을 엄선하여 안전하고 신뢰할 수 있는 서비스를 제공합니다
          </p>

          {/* Search Bar */}
          <div className="max-w-2xl mx-auto bg-gray-800 rounded-lg p-2 shadow-lg border border-gray-700 mx-3 sm:mx-auto">
            <div className="flex flex-col sm:flex-row gap-2">
              <div className="flex-1">
                <input
                  type="text"
                  placeholder="지역 또는 업소명을 검색하세요"
                  className="w-full px-3 sm:px-4 py-2.5 sm:py-3 text-white bg-gray-700 rounded-lg border-0 focus:outline-none focus:ring-2 focus:ring-pink-500 text-sm placeholder-gray-400"
                  value={searchTerm}
                  onChange={e => setSearchTerm(e.target.value)}
                />
              </div>
              <button className="bg-pink-600 text-white px-4 sm:px-6 py-2.5 sm:py-3 rounded-lg hover:bg-pink-700 whitespace-nowrap cursor-pointer text-sm">
                <i className="ri-search-line mr-1 sm:mr-2"></i>검색
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* 지역 카테고리 */}
      <section className="bg-gray-800 border-b border-gray-700">
        <div className="w-full px-3 sm:px-4 lg:px-8 py-4 sm:py-6">
          <h2 className="text-xs sm:text-sm font-medium text-white mb-3 sm:mb-4">
            지역별 찾기
          </h2>
          <div className="flex flex-wrap gap-2 mb-4">
            {regions.map(region => (
              <button
                key={region}
                onClick={() => {
                  setSelectedRegion(region);
                  setSelectedCity("전체");
                }}
                className={`px-3 py-2 rounded-lg text-sm transition-all ${
                  selectedRegion === region
                    ? "bg-pink-500 text-white"
                    : "bg-gray-700 text-gray-300 hover:bg-gray-600"
                }`}
              >
                {region}
              </button>
            ))}
          </div>

          {/* 서브 도시 선택 */}
          {selectedRegion !== "전체" && regionDistricts[selectedRegion] && (
            <div className="border-t border-gray-700 pt-4">
              <h3 className="text-xs text-gray-400 mb-2">{selectedRegion} 세부 지역</h3>
              <div className="flex flex-wrap gap-2">
                {regionDistricts[selectedRegion].map(city => (
                  <button
                    key={city}
                    onClick={() => {
                      setSelectedCity(city);
                      window.scrollTo({ top: 700, behavior: 'smooth' });
                    }}
                    className={`px-3 py-1.5 rounded text-xs transition-all ${
                      selectedCity === city
                        ? "bg-pink-400 text-white"
                        : "bg-gray-600 text-gray-300 hover:bg-gray-500"
                    }`}
                  >
                    {city}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </section>

      {/* 업종 카테고리 */}
      <section className="bg-gray-800 border-b border-gray-700">
        <div className="w-full px-3 sm:px-4 lg:px-8 py-4 sm:py-6">
          <h2 className="text-xs sm:text-sm font-medium text-white mb-3 sm:mb-4">
            업종별 찾기
          </h2>
          <div className="grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-10 gap-2">
            {serviceTypes.map(type => (
              <button
                key={type}
                onClick={() => {
                  setSelectedServiceType(type);
                  window.scrollTo({ top: 700, behavior: 'smooth' });
                }}
                className={`p-3 rounded-lg border-2 transition-all cursor-pointer text-center ${
                  selectedServiceType === type
                    ? "border-pink-500 bg-pink-500/20 text-pink-400"
                    : "border-gray-600 bg-gray-700 text-gray-300 hover:border-pink-400 hover:text-pink-400"
                }`}
              >
                <div className="flex flex-col items-center space-y-1">
                  <div className="w-8 h-8 flex items-center justify-center">
                    <i className={`text-xl ${getServiceTypeIcon(type)}`}></i>
                  </div>
                  <span className="text-xs font-medium">{type}</span>
                </div>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Shops */}
      <section className="py-6 sm:py-8 lg:py-12 bg-gray-800">
        <div className="w-full px-3 sm:px-4 lg:px-8">
          <div className="text-center mb-4 sm:mb-6 lg:mb-8">
            <h3 className="text-xl sm:text-2xl lg:text-3xl font-bold text-white mb-2 sm:mb-4">
              추천 업소
            </h3>
            <p className="text-gray-400 text-sm sm:text-base px-2">
              엄선된 프리미엄 마사지 업소를 만나보세요
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4 lg:gap-6">
            {featuredShops.slice(0, 6).map(shop => (
              <div
                key={shop.id}
                onClick={() => handleShopClick(shop.id)}
                className="bg-gray-700 rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer border border-gray-600"
                data-product-shop
              >
                <div className="relative">
                  <img
                    src={shop.image}
                    alt={shop.name}
                    className="w-full h-36 sm:h-40 lg:h-48 object-cover object-top"
                  />
                  <div className="absolute top-2 sm:top-3 lg:top-4 left-2 sm:left-3 lg:left-4">
                    <span className="bg-pink-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                      추천
                    </span>
                  </div>
                  <div className="absolute top-2 sm:top-3 lg:top-4 right-2 sm:right-3 lg:right-4">
                    <button className="bg-black/50 p-1.5 rounded-full hover:bg-black/70 cursor-pointer">
                      <i className="ri-heart-line text-white text-sm"></i>
                    </button>
                  </div>
                </div>

                <div className="p-3 sm:p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="text-sm sm:text-base lg:text-lg font-semibold text-white truncate pr-2">
                      {shop.name}
                    </h4>
                    <div className="flex items-center flex-shrink-0">
                      <i className="ri-star-fill text-yellow-400 text-sm"></i>
                      <span className="text-xs sm:text-sm text-gray-400 ml-1">
                        {shop.rating}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center text-gray-400 mb-2">
                    <i className="ri-map-pin-line text-sm mr-1"></i>
                    <span className="text-xs sm:text-sm">{shop.district}</span>
                    <span className="mx-1 sm:mx-2">•</span>
                    <span className="text-xs bg-gray-600 px-1.5 sm:px-2 py-0.5 sm:py-1 rounded">
                      {shop.category}
                    </span>
                  </div>

                  <p className="text-gray-400 text-xs sm:text-sm mb-2 sm:mb-3 line-clamp-2">
                    {shop.description}
                  </p>

                  <div className="flex flex-wrap gap-1 mb-2 sm:mb-3">
                    {shop.services.slice(0, 3).map(service => (
                      <span
                        key={service}
                        className="bg-gray-600 text-gray-300 px-1.5 sm:px-2 py-0.5 sm:py-1 rounded text-xs"
                      >
                        {service}
                      </span>
                    ))}
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-sm sm:text-base lg:text-lg font-bold text-pink-400">
                      {shop.price}
                    </span>
                    <div className="flex space-x-1 sm:space-x-2">
                      {shop.phone && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            window.open(`tel:${shop.phone}`, '_self');
                          }}
                          className="bg-gray-600 text-gray-300 px-2 py-1.5 sm:py-2 rounded-lg hover:bg-gray-500 text-xs whitespace-nowrap cursor-pointer"
                          title={`전화: ${shop.phone}`}
                        >
                          <i className="ri-phone-line"></i>
                        </button>
                      )}
                      {shop.kakao_id && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            window.open(`https://open.kakao.com/o/${shop.kakao_id}`, '_blank');
                          }}
                          className="bg-yellow-500 text-gray-900 px-2 py-1.5 sm:py-2 rounded-lg hover:bg-yellow-400 text-xs whitespace-nowrap cursor-pointer"
                          title={`카톡: ${shop.kakao_id}`}
                        >
                          <i className="ri-message-3-line"></i>
                        </button>
                      )}
                      {shop.telegram_id && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            window.open(`https://t.me/${shop.telegram_id}`, '_blank');
                          }}
                          className="bg-blue-500 text-white px-2 py-1.5 sm:py-2 rounded-lg hover:bg-blue-400 text-xs whitespace-nowrap cursor-pointer"
                          title={`텔레그램: ${shop.telegram_id}`}
                        >
                          <i className="ri-telegram-line"></i>
                        </button>
                      )}
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleShopClick(shop.id);
                        }}
                        className="bg-pink-600 text-white px-2.5 sm:px-3 lg:px-4 py-1.5 sm:py-2 rounded-lg hover:bg-pink-700 text-xs sm:text-sm whitespace-nowrap cursor-pointer"
                      >
                        상세보기
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* All Shops */}
      <section className="py-6 sm:py-8 lg:py-12 bg-gray-900">
        <div className="w-full px-3 sm:px-4 lg:px-8">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4 sm:mb-6 lg:mb-8 gap-3 sm:gap-4">
            <h3 className="text-lg sm:text-xl lg:text-2xl font-bold text-white">
              전체 업소
            </h3>
            <div className="flex items-center space-x-2">
              <span className="text-xs sm:text-sm text-gray-400">정렬:</span>
              <select className="px-2 sm:px-3 py-1 bg-gray-700 border border-gray-600 text-white rounded text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-pink-500 pr-6 sm:pr-8">
                <option>추천순</option>
                <option>평점순</option>
                <option>가격순</option>
                <option>거리순</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4 lg:gap-6">
            {filteredShops.map(shop => (
              <div
                key={shop.id}
                onClick={() => handleShopClick(shop.id)}
                className="bg-gray-700 rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer border border-gray-600"
                data-product-shop
              >
                <div className="relative">
                  <img
                    src={shop.image}
                    alt={shop.name}
                    className="w-full h-36 sm:h-40 lg:h-48 object-cover object-top"
                  />
                  {shop.featured && (
                    <div className="absolute top-2 sm:top-3 lg:top-4 left-2 sm:left-3 lg:left-4">
                      <span className="bg-pink-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                        추천
                      </span>
                    </div>
                  )}
                  <div className="absolute top-2 sm:top-3 lg:top-4 right-2 sm:right-3 lg:right-4">
                    <button className="bg-black/50 p-1.5 rounded-full hover:bg-black/70 cursor-pointer">
                      <i className="ri-heart-line text-white text-sm"></i>
                    </button>
                  </div>
                </div>

                <div className="p-3 sm:p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="text-sm sm:text-base lg:text-lg font-semibold text-white truncate pr-2">
                      {shop.name}
                    </h4>
                    <div className="flex items-center flex-shrink-0">
                      <i className="ri-star-fill text-yellow-400 text-sm"></i>
                      <span className="text-xs sm:text-sm text-gray-400 ml-1">
                        {shop.rating}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center text-gray-400 mb-2">
                    <i className="ri-map-pin-line text-sm mr-1"></i>
                    <span className="text-xs sm:text-sm">{shop.district}</span>
                    <span className="mx-1 sm:mx-2">•</span>
                    <span className="text-xs bg-gray-600 px-1.5 sm:px-2 py-0.5 sm:py-1 rounded">
                      {shop.category}
                    </span>
                  </div>

                  <div className="flex items-center text-gray-400 mb-2">
                    <i className="ri-time-line text-sm mr-1"></i>
                    <span className="text-xs sm:text-sm">{shop.hours}</span>
                  </div>

                  <p className="text-gray-400 text-xs sm:text-sm mb-2 sm:mb-3 line-clamp-2">
                    {shop.description}
                  </p>

                  <div className="flex flex-wrap gap-1 mb-2 sm:mb-3">
                    {shop.services.slice(0, 3).map(service => (
                      <span
                        key={service}
                        className="bg-gray-600 text-gray-300 px-1.5 sm:px-2 py-0.5 sm:py-1 rounded text-xs"
                      >
                        {service}
                      </span>
                    ))}
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-sm sm:text-base lg:text-lg font-bold text-pink-400">
                      {shop.price}
                    </span>
                    <div className="flex space-x-1 sm:space-x-2">
                      {shop.phone && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            window.open(`tel:${shop.phone}`, '_self');
                          }}
                          className="bg-gray-600 text-gray-300 px-2 py-1.5 sm:py-2 rounded-lg hover:bg-gray-500 text-xs whitespace-nowrap cursor-pointer"
                          title={`전화: ${shop.phone}`}
                        >
                          <i className="ri-phone-line"></i>
                        </button>
                      )}
                      {shop.kakao_id && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            window.open(`https://open.kakao.com/o/${shop.kakao_id}`, '_blank');
                          }}
                          className="bg-yellow-500 text-gray-900 px-2 py-1.5 sm:py-2 rounded-lg hover:bg-yellow-400 text-xs whitespace-nowrap cursor-pointer"
                          title={`카톡: ${shop.kakao_id}`}
                        >
                          <i className="ri-message-3-line"></i>
                        </button>
                      )}
                      {shop.telegram_id && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            window.open(`https://t.me/${shop.telegram_id}`, '_blank');
                          }}
                          className="bg-blue-500 text-white px-2 py-1.5 sm:py-2 rounded-lg hover:bg-blue-400 text-xs whitespace-nowrap cursor-pointer"
                          title={`텔레그램: ${shop.telegram_id}`}
                        >
                          <i className="ri-telegram-line"></i>
                        </button>
                      )}
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleShopClick(shop.id);
                        }}
                        className="bg-pink-600 text-white px-2.5 sm:px-3 lg:px-4 py-1.5 sm:py-2 rounded-lg hover:bg-pink-700 text-xs sm:text-sm whitespace-nowrap cursor-pointer"
                      >
                        상세보기
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {filteredShops.length === 0 && (
            <div className="text-center py-8 sm:py-12">
              <i className="ri-search-line text-3xl sm:text-4xl text-gray-500 mb-3 sm:mb-4"></i>
              <h4 className="text-base sm:text-lg font-medium text-white mb-2">
                검색 결과가 없습니다
              </h4>
              <p className="text-sm sm:text-base text-gray-400">
                다른 조건으로 검색해보세요
              </p>
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-pink-600 to-purple-600 py-8 sm:py-12 lg:py-16">
        <div className="w-full px-3 sm:px-4 lg:px-8 text-center">
          <h3 className="text-xl sm:text-2xl lg:text-3xl font-bold text-white mb-2 sm:mb-3 lg:mb-4">
            업소 운영자이신가요?
          </h3>
          <p className="text-sm sm:text-base lg:text-xl text-pink-100 mb-4 sm:mb-6 lg:mb-8 px-2 sm:px-4">
            오피인포에 업소를 등록하고 더 많은 고객을 만나보세요
          </p>
          <div className="flex flex-col sm:flex-row gap-2 sm:gap-3 lg:gap-4 justify-center px-2 sm:px-4">
            <button className="bg-white text-pink-600 px-4 sm:px-6 lg:px-8 py-2.5 sm:py-3 rounded-lg font-semibold hover:bg-gray-100 whitespace-nowrap cursor-pointer text-sm sm:text-base">
              업소 등록하기
            </button>
            <button className="border-2 border-white text-white px-4 sm:px-6 lg:px-8 py-2.5 sm:py-3 rounded-lg font-semibold hover:bg-white hover:text-pink-600 whitespace-nowrap cursor-pointer text-sm sm:text-base">
              광고 문의
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-6 sm:py-8 lg:py-12 border-t border-gray-700">
        <div className="w-full px-3 sm:px-4 lg:px-8">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 lg:gap-8">
            <div className="sm:col-span-2 lg:col-span-1">
              <h4
                className="text-base sm:text-lg lg:text-xl font-bold mb-2 sm:mb-3 lg:mb-4 text-pink-400"
                style={{ fontFamily: "Pacifico, serif" }}
              >
                오피인포
              </h4>
              <p className="text-gray-400 mb-2 sm:mb-3 lg:mb-4 text-xs sm:text-sm lg:text-base">
                전국 최고의 마사지 업소를 연결하는 신뢰할 수 있는 플랫폼입니다.
              </p>
              <div className="flex space-x-3 sm:space-x-4">
                <a href="#" className="text-gray-400 hover:text-pink-400 cursor-pointer">
                  <i className="ri-facebook-fill text-lg sm:text-xl"></i>
                </a>
                <a href="#" className="text-gray-400 hover:text-pink-400 cursor-pointer">
                  <i className="ri-instagram-line text-lg sm:text-xl"></i>
                </a>
                <a href="#" className="text-gray-400 hover:text-pink-400 cursor-pointer">
                  <i className="ri-twitter-line text-lg sm:text-xl"></i>
                </a>
              </div>
            </div>

            <div>
              <h5 className="font-semibold mb-2 sm:mb-3 lg:mb-4 text-xs sm:text-sm lg:text-base text-white">
                서비스
              </h5>
              <ul className="space-y-1 sm:space-y-2 text-gray-400 text-xs sm:text-sm">
                <li>
                  <a href="#" className="hover:text-pink-400 cursor-pointer">
                    업소 찾기
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-pink-400 cursor-pointer">
                    예약하기
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-pink-400 cursor-pointer">
                    리뷰 작성
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-pink-400 cursor-pointer">
                    이벤트
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <h5 className="font-semibold mb-2 sm:mb-3 lg:mb-4 text-xs sm:text-sm lg:text-base text-white">
                업소 운영자
              </h5>
              <ul className="space-y-1 sm:space-y-2 text-gray-400 text-xs sm:text-sm">
                <li>
                  <a href="#" className="hover:text-pink-400 cursor-pointer">
                    업소 등록
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-pink-400 cursor-pointer">
                    광고 문의
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-pink-400 cursor-pointer">
                    관리자 페이지
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-pink-400 cursor-pointer">
                    수수료 안내
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <h5 className="font-semibold mb-2 sm:mb-3 lg:mb-4 text-xs sm:text-sm lg:text-base text-white">
                고객센터
              </h5>
              <ul className="space-y-1 sm:space-y-2 text-gray-400 text-xs sm:text-sm">
                <li>
                  <a href="#" className="hover:text-pink-400 cursor-pointer">
                    자주 묻는 질문
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-pink-400 cursor-pointer">
                    공지사항
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-pink-400 cursor-pointer">
                    문의하기
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-pink-400 cursor-pointer">
                    신고하기
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-700 mt-4 sm:mt-6 lg:mt-8 pt-4 sm:pt-6 lg:pt-8 flex flex-col md:flex-row justify-between items-center gap-3 sm:gap-4">
            <p className="text-gray-400 text-xs sm:text-sm text-center md:text-left">
              © 2024 오피인포. All rights reserved.
            </p>
            <div className="flex flex-wrap justify-center md:justify-end space-x-3 sm:space-x-4 lg:space-x-6">
              <a href="#" className="text-gray-400 hover:text-pink-400 text-xs sm:text-sm cursor-pointer">
                이용약관
              </a>
              <a href="#" className="text-gray-400 hover:text-pink-400 text-xs sm:text-sm cursor-pointer">
                개인정보처리방침
              </a>
              <a href="https://readdy.ai/?origin=logo" className="text-gray-400 hover:text-pink-400 text-xs sm:text-sm cursor-pointer">
                Powered by Readdy
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

function getServiceTypeIcon(serviceType: string): string {
  const iconMap: { [key: string]: string } = {
    "전체보기": "ri-home-line",
    "오피스텔": "ri-building-line",
    "건마": "ri-hand-heart-line",
    "핸플/립": "ri-heart-pulse-line",
    "유흥/밤": "ri-goblet-line",
    "유흥주점": "ri-drink-2-line",
    "안마": "ri-body-scan-line",
    "휴게텔": "ri-hotel-bed-line",
    "키스방": "ri-emotion-line",
    "토핑/리얼": "ri-star-line"
  };
  return iconMap[serviceType] || "ri-store-line";
}

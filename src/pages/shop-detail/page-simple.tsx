import { useParams, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import shopsData from '../../data/shops_data.json';

export default function ShopDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'profile' | 'comments' | 'reviews'>('profile');

  // 실제 크롤링 데이터에서 해당 ID의 업소 찾기
  const shop = shopsData.find((s: any) => s.id === parseInt(id || '1'));

  if (!shop) {
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

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 shadow-sm border-b border-gray-700 sticky top-0 z-50">
        <div className="w-full px-3 sm:px-4 lg:px-8">
          <div className="flex justify-between items-center h-14 sm:h-16">
            <div className="flex items-center space-x-3">
              <button
                onClick={() => navigate('/')}
                className="p-2 text-gray-300 hover:text-white cursor-pointer"
              >
                <i className="ri-arrow-left-line text-xl"></i>
              </button>
              <h1 className="text-lg sm:text-xl font-bold text-pink-400">
                오피인포
              </h1>
            </div>
          </div>
        </div>
      </header>

      {/* 탭 메뉴 */}
      <section className="bg-gray-800 border-b border-gray-700 sticky top-14 sm:top-16 z-40">
        <div className="w-full px-3 sm:px-4 lg:px-8">
          <div className="flex border-b border-gray-700">
            <button
              onClick={() => setActiveTab('profile')}
              className={`flex-1 py-3 text-sm sm:text-base font-medium transition-colors ${
                activeTab === 'profile'
                  ? 'text-pink-400 border-b-2 border-pink-400'
                  : 'text-gray-400 hover:text-gray-300'
              }`}
            >
              <i className="ri-user-line mr-2"></i>
              프로필
            </button>
            <button
              onClick={() => setActiveTab('comments')}
              className={`flex-1 py-3 text-sm sm:text-base font-medium transition-colors ${
                activeTab === 'comments'
                  ? 'text-pink-400 border-b-2 border-pink-400'
                  : 'text-gray-400 hover:text-gray-300'
              }`}
            >
              <i className="ri-chat-3-line mr-2"></i>
              댓글
            </button>
            <button
              onClick={() => setActiveTab('reviews')}
              className={`flex-1 py-3 text-sm sm:text-base font-medium transition-colors ${
                activeTab === 'reviews'
                  ? 'text-pink-400 border-b-2 border-pink-400'
                  : 'text-gray-400 hover:text-gray-300'
              }`}
            >
              <i className="ri-star-line mr-2"></i>
              후기
            </button>
          </div>
        </div>
      </section>

      {/* 탭 컨텐츠 - 프로필 */}
      {activeTab === 'profile' && shop.url && (
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
            <div className="bg-gray-900 rounded-lg overflow-hidden" style={{ height: '80vh' }}>
              <iframe
                src={shop.url}
                className="w-full h-full border-0"
                title={shop.name}
              />
            </div>
          </div>
        </section>
      )}

      {/* 탭 컨텐츠 - 댓글 */}
      {activeTab === 'comments' && (
        <section className="bg-gray-800">
          <div className="w-full px-3 sm:px-4 lg:px-8 py-4">
            <h3 className="text-white text-base font-semibold mb-4">댓글</h3>

            {/* 댓글 작성 폼 */}
            <div className="bg-gray-700 rounded-lg p-4 mb-4">
              <textarea
                placeholder="댓글을 작성하세요..."
                className="w-full bg-gray-600 text-white p-3 rounded-lg border border-gray-500 focus:border-pink-400 focus:outline-none resize-none"
                rows={3}
              ></textarea>
              <div className="flex justify-end mt-2">
                <button className="bg-pink-500 text-white px-4 py-2 rounded-lg hover:bg-pink-600">
                  댓글 작성
                </button>
              </div>
            </div>

            {/* 댓글 목록 */}
            <div className="space-y-4">
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="flex items-center mb-2">
                  <div className="w-10 h-10 bg-gray-600 rounded-full flex items-center justify-center mr-3">
                    <i className="ri-user-line text-gray-400"></i>
                  </div>
                  <div>
                    <div className="text-white font-medium">사용자1</div>
                    <div className="text-gray-400 text-xs">2024-01-08</div>
                  </div>
                </div>
                <p className="text-gray-300">여기 정말 좋아요! 추천합니다.</p>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* 탭 컨텐츠 - 후기 */}
      {activeTab === 'reviews' && (
        <section className="bg-gray-800">
          <div className="w-full px-3 sm:px-4 lg:px-8 py-4">
            <h3 className="text-white text-base font-semibold mb-4">후기</h3>

            {/* 후기 작성 폼 */}
            <div className="bg-gray-700 rounded-lg p-4 mb-4">
              <div className="mb-3">
                <label className="text-white text-sm mb-2 block">별점</label>
                <div className="flex space-x-2">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button key={star} className="text-2xl text-gray-500 hover:text-yellow-400">
                      <i className="ri-star-fill"></i>
                    </button>
                  ))}
                </div>
              </div>
              <textarea
                placeholder="후기를 작성하세요..."
                className="w-full bg-gray-600 text-white p-3 rounded-lg border border-gray-500 focus:border-pink-400 focus:outline-none resize-none"
                rows={4}
              ></textarea>
              <div className="flex justify-end mt-2">
                <button className="bg-pink-500 text-white px-4 py-2 rounded-lg hover:bg-pink-600">
                  후기 등록
                </button>
              </div>
            </div>

            {/* 후기 목록 */}
            <div className="space-y-4">
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center">
                    <div className="w-10 h-10 bg-gray-600 rounded-full flex items-center justify-center mr-3">
                      <i className="ri-user-line text-gray-400"></i>
                    </div>
                    <div>
                      <div className="text-white font-medium">고객님</div>
                      <div className="text-gray-400 text-xs">2024-01-08</div>
                    </div>
                  </div>
                  <div className="flex">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <i key={star} className="ri-star-fill text-yellow-400 text-sm"></i>
                    ))}
                  </div>
                </div>
                <p className="text-gray-300">서비스가 매우 만족스러웠습니다. 다음에도 재방문 의향 있습니다!</p>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* 기본 정보 */}
      <section className="bg-gray-800 border-b border-gray-700">
        <div className="w-full px-3 sm:px-4 lg:px-8 py-4">
          <h2 className="text-2xl font-bold text-white mb-2">{shop.name}</h2>
          <div className="flex items-center text-gray-400 mb-3">
            <i className="ri-map-pin-line mr-2"></i>
            <span>{shop.district}, {shop.location}</span>
          </div>
          <div className="flex items-center text-gray-400 mb-3">
            <i className="ri-time-line mr-2"></i>
            <span>{shop.hours}</span>
          </div>
          {shop.phone && (
            <div className="flex items-center text-gray-400 mb-3">
              <i className="ri-phone-line mr-2"></i>
              <span>{shop.phone}</span>
            </div>
          )}
          <p className="text-gray-300 mb-4">{shop.description}</p>

          {/* 연락 버튼 */}
          <div className="flex space-x-2">
            {shop.phone && (
              <button
                onClick={() => window.open(`tel:${shop.phone}`, '_self')}
                className="flex-1 bg-gray-600 text-white px-4 py-3 rounded-lg hover:bg-gray-500 flex items-center justify-center gap-2"
              >
                <i className="ri-phone-line"></i>
                전화하기
              </button>
            )}
            {shop.kakao_id && (
              <button
                onClick={() => window.open(`https://open.kakao.com/o/${shop.kakao_id}`, '_blank')}
                className="flex-1 bg-yellow-500 text-gray-900 px-4 py-3 rounded-lg hover:bg-yellow-400 flex items-center justify-center gap-2"
              >
                <i className="ri-message-3-line"></i>
                카톡
              </button>
            )}
            {shop.telegram_id && (
              <button
                onClick={() => window.open(`https://t.me/${shop.telegram_id}`, '_blank')}
                className="flex-1 bg-blue-500 text-white px-4 py-3 rounded-lg hover:bg-blue-400 flex items-center justify-center gap-2"
              >
                <i className="ri-telegram-line"></i>
                텔레그램
              </button>
            )}
          </div>
        </div>
      </section>

      {/* 상세 이미지 갤러리 - 세로 나열 */}
      {shop.gallery && shop.gallery.length > 0 && (
        <section className="bg-gray-900">
          <div className="w-full max-w-4xl mx-auto px-0 py-0">
            <div className="flex flex-col gap-0">
              {shop.gallery.map((image: string, index: number) => (
                <div
                  key={index}
                  className="w-full"
                >
                  <img
                    src={image}
                    alt={`Gallery ${index + 1}`}
                    className="w-full h-auto object-contain"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = shop.image;
                    }}
                  />
                </div>
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
}

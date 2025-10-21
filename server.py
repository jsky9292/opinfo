#!/usr/bin/env python3
"""
간단한 로컬 웹 서버 - 크롤링 데이터 확인용
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # 대전 데이터 읽기
            try:
                with open('daejeon_shops_data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)

                html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>업소 정보 - 로컬 뷰어</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Malgun Gothic', sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ text-align: center; color: #333; margin-bottom: 30px; }}
        .stats {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; text-align: center; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }}
        .card {{ background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .card img {{ width: 100%; height: 250px; object-fit: cover; }}
        .card-body {{ padding: 15px; }}
        .title {{ font-size: 18px; font-weight: bold; color: #333; margin-bottom: 10px; }}
        .info {{ font-size: 14px; color: #666; margin: 5px 0; }}
        .location {{ color: #ff4444; font-weight: bold; }}
        .description {{ color: #888; font-size: 13px; margin-top: 10px; line-height: 1.4; }}
        .gallery {{ display: flex; gap: 5px; margin-top: 10px; overflow-x: auto; }}
        .gallery img {{ width: 60px; height: 60px; object-fit: cover; border-radius: 4px; cursor: pointer; }}
        .no-image {{ background: #ddd; height: 250px; display: flex; align-items: center; justify-content: center; color: #999; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏢 업소 정보 뷰어</h1>
        <div class="stats">
            <h2>총 {len(data)}개 업소</h2>
        </div>
        <div class="grid">
"""

                for shop in data:
                    gallery = shop.get('gallery', [])
                    thumbnail = shop.get('image', '')

                    img_html = f'<img src="{thumbnail}" alt="{shop.get("name", "")}">' if thumbnail else '<div class="no-image">이미지 없음</div>'

                    gallery_html = ''
                    if gallery:
                        gallery_html = '<div class="gallery">'
                        for img in gallery[:10]:  # 최대 10개만
                            gallery_html += f'<img src="{img}" alt="갤러리">'
                        gallery_html += f'<span style="color:#999; font-size:12px; align-self:center;">+{len(gallery)}장</span></div>'

                    url = shop.get('url', '')
                    url_link = f'<div class="info">🔗 <a href="{url}" target="_blank" style="color:#0066cc;">상세 페이지 보기</a></div>' if url else ''

                    html += f"""
            <div class="card">
                {img_html}
                <div class="card-body">
                    <div class="title">{shop.get('name', '업소명 없음')}</div>
                    <div class="info"><span class="location">{shop.get('location', '')} {shop.get('district', '')}</span></div>
                    <div class="info">⏰ {shop.get('hours', '정보 없음')}</div>
                    <div class="info">📞 {shop.get('phone', '정보 없음')}</div>
                    {url_link}
                    <div class="description">{shop.get('description', '')}</div>
                    {gallery_html}
                </div>
            </div>
"""

                html += """
        </div>
    </div>
</body>
</html>
"""
                self.wfile.write(html.encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(f'<h1>오류: {e}</h1>'.encode('utf-8'))

        else:
            super().do_GET()

if __name__ == '__main__':
    PORT = 8000
    server = HTTPServer(('localhost', PORT), MyHandler)
    print(f'\n✅ 서버 시작: http://localhost:{PORT}')
    print(f'📂 현재 디렉토리: {os.getcwd()}')
    print('⛔ 종료하려면 Ctrl+C를 누르세요\n')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n\n서버 종료됨')
        server.shutdown()

# Hướng Dẫn Deploy Website Lên Render

## Bước 1: Push Code Lên GitHub

\`\`\`bash
git add website/
git commit -m "Add landing page website"
git push origin branch-PY
\`\`\`

## Bước 2: Tạo Static Site Trên Render

1. Vào https://dashboard.render.com/
2. Nhấn **New** → **Static Site**
3. Connect repository: `Bao2k5/laptrinhpython`
4. Cấu hình:
   - **Name**: `flappybird-website`
   - **Branch**: `branch-PY`
   - **Root Directory**: Leave empty
   - **Build Command**: Leave empty
   - **Publish Directory**: `website`
5. Nhấn **Create Static Site**

## Bước 3: Đợi Deploy

Render sẽ tự động deploy website. Sau 1-2 phút, bạn sẽ có link:

\`\`\`
https://flappybird-website.onrender.com
\`\`\`

## Bước 4: Test Website

Vào link và kiểm tra:
- ✅ Hero section hiển thị đúng
- ✅ Stats load từ API
- ✅ Leaderboard hiển thị top 10
- ✅ Download button hoạt động

## Lưu Ý

### CORS Issue
Nếu leaderboard không load, cần thêm CORS headers vào server API:

Trong `app.py`:
\`\`\`python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS
\`\`\`

Và thêm vào `requirements.txt`:
\`\`\`
flask-cors
\`\`\`

### Custom Domain (Optional)
Sau khi deploy, bạn có thể:
1. Settings → Custom Domain
2. Thêm domain của bạn
3. Cập nhật DNS

## Troubleshooting

### Website không load
- Kiểm tra Publish Directory = `website`
- Kiểm tra file `index.html` có trong `website/`

### Leaderboard không hiển thị
- Kiểm tra API server đang chạy
- Kiểm tra CORS đã enable
- Mở DevTools → Console để xem lỗi

### Download button không hoạt động
- Cập nhật link trong `js/main.js`
- Upload .exe lên Google Drive
- Lấy link chia sẻ

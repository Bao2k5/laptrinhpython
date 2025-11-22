# Trang Web Giới Thiệu Game Flappy Bird

Trang web landing page để phân phối game desktop Flappy Bird.

## 🌐 Tính Năng

- ✅ Hero section với background đẹp
- ✅ Thống kê realtime (người chơi, điểm cao nhất)
- ✅ Bảng xếp hạng top 10 từ server
- ✅ Nút download game
- ✅ Hướng dẫn cài đặt và chơi
- ✅ Responsive design (mobile-friendly)

## 📁 Cấu Trúc

\`\`\`
website/
├── index.html          # Trang chủ
├── hero-bg.png         # Background hero section
├── css/
│   └── style.css      # Styling
└── js/
    └── main.js        # JavaScript
\`\`\`

## 🚀 Cách Sử Dụng

### 1. Test Local

Mở file `index.html` bằng trình duyệt:

\`\`\`bash
cd website
start index.html
\`\`\`

Hoặc dùng Live Server trong VS Code.

### 2. Cập Nhật Download Link

Sau khi upload file `.exe` lên Google Drive:

1. Lấy link chia sẻ
2. Mở `js/main.js`
3. Tìm dòng: `const downloadLink = 'https://drive.google.com/...'`
4. Thay bằng link của bạn

### 3. Deploy Lên Web

#### Option A: Netlify (Khuyến nghị)
1. Vào https://netlify.com
2. Drag & drop thư mục `website/`
3. Deploy xong!

#### Option B: Render Static Site
1. Push code lên GitHub
2. Tạo Static Site trên Render
3. Point đến thư mục `website/`

#### Option C: GitHub Pages
1. Push code lên GitHub
2. Settings → Pages
3. Chọn branch và thư mục `website/`

## 🎨 Customization

### Thay đổi màu sắc
Sửa trong `css/style.css`:
- `#667eea` và `#764ba2` - Màu chủ đạo
- `#f093fb` và `#f5576c` - Màu nút download

### Thay đổi API URL
Sửa trong `js/main.js`:
\`\`\`javascript
const API_BASE_URL = 'https://your-server.com';
\`\`\`

## 📊 Features

- **Auto-refresh leaderboard**: Cập nhật mỗi 30 giây
- **Smooth animations**: Hiệu ứng mượt mà
- **Responsive**: Tự động điều chỉnh cho mobile
- **SEO-friendly**: Meta tags đầy đủ

## 🔗 Links

- Game Desktop: `desktop/dist/FlappyBird.exe`
- API Server: https://flappybird-duatop.onrender.com
- GitHub: https://github.com/Bao2k5/laptrinhpython

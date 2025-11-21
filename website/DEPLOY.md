# Hướng Dẫn Deploy Đầy Đủ

## 🎯 Bạn Cần Deploy 2 Services

### 1. API Server (Đã có - laptrinthpython-3)
- ✅ Đã deploy tại: https://laptrinthpython-3.onrender.com
- ✅ Serve API cho leaderboard
- ✅ Kết nối MongoDB
- ⚠️ **Đang redeploy** sau khi fix build.py

### 2. Website (Cần tạo mới)
- ❌ Chưa deploy
- 📁 Code ở folder `website/`
- 🎯 Sẽ là trang chủ để tải game

---

## 🚀 Cách Deploy Website (Static Site)

### Bước 1: Vào Render Dashboard
https://dashboard.render.com/

### Bước 2: Tạo Static Site Mới
1. Nhấn **New +** (góc trên bên phải)
2. Chọn **Static Site**

### Bước 3: Connect Repository
1. Chọn repository: **Bao2k5/laptrinhpython**
2. Nhấn **Connect**

### Bước 4: Cấu Hình
Điền thông tin sau:

- **Name**: `flappybird-website` (hoặc tên bạn thích)
- **Branch**: `branch-PY`
- **Root Directory**: (để trống)
- **Build Command**: (để trống)
- **Publish Directory**: `website`

### Bước 5: Deploy
1. Nhấn **Create Static Site**
2. Đợi 1-2 phút
3. Website sẽ live tại: `https://flappybird-website.onrender.com`

---

## ✅ Sau Khi Deploy Xong

Bạn sẽ có:

1. **API Server**: https://laptrinthpython-3.onrender.com
   - Serve leaderboard
   - Lưu điểm

2. **Website**: https://flappybird-website.onrender.com
   - Trang chủ game
   - Download button
   - Bảng xếp hạng

---

## 🔧 Troubleshooting

### API Server Build Failed
- ✅ Đã fix - Render đang redeploy
- Đợi vài phút để deploy xong

### Website Không Hiển Thị
- Kiểm tra **Publish Directory** = `website`
- Kiểm tra **Branch** = `branch-PY`

### Leaderboard Không Load
- Đợi API server deploy xong
- Kiểm tra API URL trong `website/js/main.js`

---

## 📋 Checklist

- [x] API Server đã có
- [x] Fix build.py issue
- [x] Push code lên GitHub
- [ ] Tạo Static Site cho website
- [ ] Deploy website
- [ ] Test tất cả tính năng
- [ ] Chia sẻ link!

---

**Bây giờ hãy tạo Static Site theo hướng dẫn trên!** 🚀

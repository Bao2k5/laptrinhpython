# 🎮 HƯỚNG DẪN CÀI ĐẶT 4 MÀN CHƠI CHO FLAPPY BIRD

## 📋 YÊU CẦU ẢNH BACKGROUND

Bạn cần chuẩn bị **4 ảnh background** và đặt vào thư mục `imgs/`:

### Tên file (BẮT BUỘC):
- `bg_level1.png` - Màn 1 (EASY - Dễ)
- `bg_level2.png` - Màn 2 (MEDIUM - Trung bình)  
- `bg_level3.png` - Màn 3 (HARD - Khó)
- `bg_level4.png` - Màn 4 (EXTREME - Cực khó)

### Kích thước khuyến nghị:
- **288 x 512 pixels** (kích thước gốc)
- Hoặc **576 x 1024 pixels** (đã scale 2x)
- Game sẽ tự động scale2x nếu bạn dùng ảnh nhỏ

### Gợi ý màu sắc/theme cho từng màn:
1. **Level 1 (EASY)**: 🌅 Ban ngày - Trời xanh sáng, mây trắng
2. **Level 2 (MEDIUM)**: 🌆 Hoàng hôn - Trời cam, vàng
3. **Level 3 (HARD)**: 🌃 Ban đêm - Trời tối, có sao
4. **Level 4 (EXTREME)**: 🌌 Vũ trụ/Địa ngục - Đỏ, tím, đen

### Lưu ý:
- Nếu thiếu ảnh nào, game sẽ tự động dùng `bg.png` làm thay thế
- Định dạng: PNG hoặc JPG đều được

---

## 🎯 HỆ THỐNG 4 MÀN CHƠI

### Điểm qua màn:
- **Level 1**: Score 0-9 điểm
- **Level 2**: Score 10-24 điểm  
- **Level 3**: Score 25-49 điểm
- **Level 4**: Score 50+ điểm

### Độ khó mỗi màn:

| Level | Tốc độ ống | Khoảng cách ống | Tốc độ nền | Độ khó |
|-------|-----------|----------------|-----------|--------|
| 1     | 5         | 200px          | 5         | ⭐     |
| 2     | 6         | 180px          | 6         | ⭐⭐   |
| 3     | 7         | 160px          | 7         | ⭐⭐⭐ |
| 4     | 8         | 140px          | 8         | ⭐⭐⭐⭐|

### Màu hiển thị level:
- Level 1: 🟢 Xanh lá (EASY)
- Level 2: 🟡 Vàng (MEDIUM)
- Level 3: 🟠 Cam (HARD)  
- Level 4: 🔴 Đỏ (EXTREME)

---

## 🚀 CÁCH SỬ DỤNG

### Bước 1: Chuẩn bị ảnh background
```
NEAT-Flappy-bird/
├── imgs/
│   ├── bg_level1.png  ← Thêm file này
│   ├── bg_level2.png  ← Thêm file này
│   ├── bg_level3.png  ← Thêm file này
│   ├── bg_level4.png  ← Thêm file này
│   ├── bird1.png
│   ├── bird2.png
│   ├── bird3.png
│   ├── pipe.png
│   └── base.png
```

### Bước 2: Chạy game
```cmd
cd C:\Users\Bao\Desktop\Flappybird\NEAT-Flappy-bird
python flappy_bird_levels.py
```

---

## 🎨 GỢI Ý TẢI ẢNH BACKGROUND

### Option 1: Tự vẽ/photoshop
- Dùng Photoshop, GIMP, hoặc Paint.NET
- Tạo ảnh 288x512px
- Vẽ background phù hợp với theme

### Option 2: Tải ảnh có sẵn
Tìm kiếm trên:
- OpenGameArt.org
- itch.io (free game assets)
- Kenney.nl (free assets)
- Pixabay, Unsplash (ảnh miễn phí)

### Option 3: Dùng AI tạo ảnh
- DALL-E, Midjourney
- Stable Diffusion
- Bing Image Creator (miễn phí)

Prompt gợi ý:
- "pixel art sky background for flappy bird game, daytime, blue sky"
- "8-bit sunset background for mobile game, orange sky"
- "retro night sky background, stars, pixel art style"
- "space background for game, purple and red, pixel art"

---

## ✨ TÍNH NĂNG ĐÃ CÓ

✅ 4 màn chơi với độ khó tăng dần
✅ Background tự động đổi theo level
✅ Hiển thị "LEVEL UP!" khi qua màn
✅ Màu sắc level thay đổi theo độ khó
✅ Tốc độ game tăng dần
✅ Khoảng cách ống giảm dần (khó hơn)
✅ Tự động fallback về bg.png nếu thiếu ảnh
✅ AI NEAT vẫn hoạt động bình thường

---

## 🔧 TÙY CHỈNH

Nếu muốn thay đổi điểm qua màn hoặc độ khó, sửa trong file `flappy_bird_levels.py`:

```python
# Dòng 38-40: Thay đổi điểm qua màn
LEVEL_THRESHOLDS = [0, 10, 25, 50]  # Level 1, 2, 3, 4

# Dòng 49-54: Thay đổi độ khó
settings = {
    1: {"pipe_vel": 5, "pipe_gap": 200, "base_vel": 5},
    2: {"pipe_vel": 6, "pipe_gap": 180, "base_vel": 6},
    3: {"pipe_vel": 7, "pipe_gap": 160, "base_vel": 7},
    4: {"pipe_vel": 8, "pipe_gap": 140, "base_vel": 8}
}
```

---

## 📝 GHI CHÚ

- Game sẽ tự động kiểm tra và load background khi khởi động
- Nếu thiếu ảnh sẽ hiện thông báo: "⚠️ bg_levelX.png not found"
- AI sẽ học chơi qua tất cả 4 level tự động
- Background đổi ngay lập tức khi đủ điểm

---

Chúc bạn chơi game vui vẻ! 🎮🐦


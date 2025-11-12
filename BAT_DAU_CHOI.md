# 🎤 HƯỚNG DẪN CHƠI NHANH - BREATH CONTROL

## ✅ CÀI ĐẶT XONG RỒI!

Thư viện đã sẵn sàng:
- ✅ sounddevice đã cài
- ✅ pygame đã có
- ✅ numpy đã có

---

## 🚀 CHƠI NGAY BÂY GIỜ!

### Cách 1: Double-click file
```
PLAY_BREATH.bat
```

### Cách 2: Mở CMD và gõ
```bash
cd C:\Users\Bao\Desktop\Flappybird\NEAT-Flappy-bird
python breath_game.py
```

---

## 🎮 CÁCH CHƠI

### Khi game khởi động:

1. **Calibration (2 giây đầu)**
   - 🤫 Giữ im lặng 2 giây
   - Game đo tiếng ồn nền
   
2. **Nhấn SPACE để bắt đầu**

3. **Điều khiển:**
   - 🔊 **THỔI MẠNH** → Chim bay cao ↑↑↑
   - 💨 **THỞ ĐỀU** → Chim giữ độ cao ⟷
   - 🤐 **IM LẶNG** → Chim rơi xuống ↓↓↓

### 📊 Nhìn vào màn hình:
- **Thanh màu bên trái**: Hiển thị mức âm thanh của bạn
  - Đỏ = Đang thổi mạnh (Jump)
  - Vàng = Đang thở đều (Hover)
  - Xám = Im lặng (Fall)

---

## 🧪 TEST TRƯỚC KHI CHƠI

Nếu muốn test xem micro hoạt động tốt không:

```bash
TEST_MICROPHONE.bat
```

Hoặc:
```bash
python breath_controller.py
```

Bạn sẽ thấy thanh volume:
```
Volume: [████████░░░░░░] 0.27 | Action: hover
```

Thử thổi hoặc nói to, thanh sẽ đầy lên!

---

## 💡 MẸO CHƠI

1. **Tìm độ mạnh vừa phải**
   - Đừng thổi quá mạnh
   - Thổi ngắn, nhẹ nhàng

2. **Thở đều để hover**
   - Thở ra nhẹ nhàng
   - Giữ đều đặn để chim không bay lên cao

3. **Im lặng để rơi nhanh**
   - Ngậm miệng lại
   - Chim sẽ rơi qua ống

4. **Chơi ở chỗ yên tĩnh**
   - Tắt nhạc nền
   - Tránh tiếng ồn

---

## ❌ NẾU GẶP LỖI

### "No microphone found"
→ Cắm tai nghe/micro vào máy
→ Settings → Privacy → Microphone → Bật quyền

### Chim cứ bay liên tục
→ Môi trường quá ồn
→ Chạy lại và giữ im lặng khi calibrate

### Chim không bay
→ Thổi to hơn
→ Mic có thể bị yếu

---

## ⌨️ PHÍM TẮT

- **ESC**: Thoát game
- **SPACE**: Bắt đầu game (khi ở menu)

---

## 🎉 BẮT ĐẦU CHƠI!

1. Double-click: `PLAY_BREATH.bat`
2. Giữ im lặng 2 giây (calibration)
3. Nhấn SPACE
4. Thổi vào mic để chim bay!

**HAVE FUN! 🎮🎤🐦**


# 🎤 HƯỚNG DẪN CHƠI FLAPPY BIRD BẰNG HỞI THỞ / GIỌNG NÓI

## 🚀 Cài đặt nhanh

### Bước 1: Cài đặt thư viện
```bash
pip install sounddevice
```

Hoặc cài tất cả thư viện:
```bash
pip install -r requirments.txt
```

### Bước 2: Chạy game
**Windows:**
```bash
PLAY_BREATH.bat
```

**Hoặc chạy trực tiếp:**
```bash
python breath_game.py
```

---

## 🎮 CÁCH CHƠI

### 🎤 Điều khiển bằng hơi thở / giọng nói:

1. **🔊 THỔI MẠNH / NÓI TO** 
   - Chim bay cao lên
   - Volume > 35% → Jump!

2. **💨 GIỮ HƠI ĐỀU / NÓI NHẸ**
   - Chim giữ độ cao (hover)
   - Volume 15-35% → Hover

3. **🤐 IM LẶNG**
   - Chim rơi xuống
   - Volume < 15% → Fall

### 📊 Thanh âm lượng:
- **Thanh màu xanh bên trái** hiển thị mức âm thanh hiện tại
- **Vạch đỏ** = ngưỡng Jump (35%)
- **Vạch vàng** = ngưỡng Hover (15%)

---

## 🧪 TEST MICROPHONE

Trước khi chơi, test microphone hoạt động tốt chưa:

```bash
python breath_controller.py
```

Bạn sẽ thấy thanh volume như này:
```
Volume: [████████░░░░░░░░░░░░░░░░░░░░] 0.27 | Action: hover
```

---

## ⚙️ TÙY CHỈNH ĐỘ NHẠY

Nếu game quá nhạy hoặc quá khó, sửa trong file `breath_controller.py`:

```python
# Dòng ~35-37
self.threshold_jump = 0.35      # Giảm xuống 0.25 nếu muốn nhạy hơn
self.threshold_hover_min = 0.15  # Tăng lên 0.20 nếu chim cứ bay
self.threshold_hover_max = 0.35
```

---

## 🛠️ TROUBLESHOOTING

### ❌ Lỗi: "No microphone found"
**Giải pháp:**
1. Kiểm tra microphone đã cắm chưa
2. Cho phép Windows/app truy cập microphone:
   - Settings → Privacy → Microphone → Bật
3. Chọn đúng microphone mặc định trong Windows

### ❌ Lỗi: "Could not import sounddevice"
**Giải pháp:**
```bash
pip install sounddevice --upgrade
```

### ❌ Chim cứ bay liên tục hoặc không bay
**Giải pháp:**
1. Chạy lại calibration:
   - Game sẽ tự động calibrate khi khởi động
   - Giữ im lặng trong 2 giây khi calibrate
2. Kiểm tra môi trường:
   - Tắt nhạc nền / quạt gió
   - Chơi ở phòng yên tĩnh

### ❌ Input bị giật lag
**Giải pháp:**
- Tăng `smoothing_window` trong `breath_controller.py`:
```python
# Dòng ~26
controller = BreathController(smoothing_window=8)  # Mặc định là 5
```

---

## 🎯 MẸO CHƠI HAY

1. **Tập thở đều:** Giữ hơi thở đều đặn để chim hover ổn định
2. **Thổi ngắn:** Thổi nhẹ, ngắn để nhảy vừa phải
3. **Im lặng:** Ngậm miệng khi muốn chim rơi nhanh
4. **Practice makes perfect:** Tập vài lần để quen với độ nhạy

---

## 📝 THÔNG TIN KỸ THUẬT

### Công nghệ:
- **Python 3.x**
- **Pygame** - Game engine
- **Sounddevice** - Real-time audio input
- **NumPy** - Signal processing

### Cách hoạt động:
1. Microphone thu âm liên tục (chunks 50ms)
2. Tính RMS (Root Mean Square) volume
3. Trừ noise floor (tiếng ồn nền)
4. Smoothing qua moving average
5. So sánh với ngưỡng → Action (jump/hover/fall)

### Hiệu suất:
- Audio latency: ~50-100ms
- Frame rate: 30 FPS
- CPU usage: ~5-10%

---

## 🔬 MODE NÂNG CAO (Sắp có)

- [ ] Voice commands: "UP", "DOWN", "STOP"
- [ ] ML model nhận dạng pattern hơi thở
- [ ] Multiplayer với 2 microphones
- [ ] Recording & replay breath patterns

---

## 📞 HỖ TRỢ

Gặp vấn đề? Tạo issue trên GitHub hoặc liên hệ!

**Happy breathing! 🎮🎤**


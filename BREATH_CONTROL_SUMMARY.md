# 🎤 FLAPPY BIRD - BREATH CONTROL EDITION

## ✨ TÍNH NĂNG MỚI ĐÃ HOÀN THÀNH

### 📁 Files đã tạo:

1. **breath_controller.py** - Module xử lý microphone input
   - Thu âm real-time từ micro
   - Đo cường độ âm thanh (volume)
   - Chuyển đổi volume thành action (jump/hover/fall)
   - Có smoothing để tránh giật lag
   - Auto-calibration để loại bỏ tiếng ồn nền

2. **breath_game.py** - Game Flappy Bird điều khiển bằng hơi thở
   - Player mode (1 người chơi)
   - Điều khiển chim bằng hơi thở / giọng nói
   - Thanh volume indicator hiển thị real-time
   - Instructions trong game
   - Game over & restart

3. **PLAY_BREATH.bat** - File chạy nhanh cho Windows
   - Double-click để chơi ngay!

4. **TEST_MICROPHONE.bat** - Test microphone trước khi chơi
   - Kiểm tra xem micro hoạt động tốt không

5. **HUONG_DAN_BREATH_CONTROL.md** - Hướng dẫn đầy đủ
   - Cách cài đặt
   - Cách chơi
   - Troubleshooting
   - Tips & tricks

6. **requirments.txt** - Đã cập nhật
   - Thêm sounddevice library

---

## 🚀 CÁCH SỬ DỤNG

### Bước 1: Cài đặt thư viện (ĐÃ XONG ✅)
```bash
pip install sounddevice
```
✅ Đã cài đặt thành công: sounddevice-0.5.3

### Bước 2: Test microphone
Double-click file: **TEST_MICROPHONE.bat**

Hoặc chạy:
```bash
python breath_controller.py
```

Bạn sẽ thấy thanh volume như này:
```
Volume: [████████░░░░░░░░░░░░░░░░░░░░] 0.27 | Action: hover
```

### Bước 3: Chơi game!
Double-click file: **PLAY_BREATH.bat**

Hoặc chạy:
```bash
python breath_game.py
```

---

## 🎮 CÁCH CHƠI

### 🎤 Điều khiển:

| Hành động | Kết quả | Volume |
|-----------|---------|--------|
| 🔊 **THỔI MẠNH / NÓI TO** | Chim bay cao | > 35% |
| 💨 **HƠI ĐỀU / NÓI NHẸ** | Chim giữ độ cao | 15-35% |
| 🤐 **IM LẶNG** | Chim rơi xuống | < 15% |

### 📊 Giao diện:
- **Thanh volume bên trái màu**: Hiển thị mức âm thanh hiện tại
- **Vạch đỏ**: Ngưỡng Jump (35%)
- **Vạch vàng**: Ngưỡng Hover (15%)
- **Text màu**: Hiển thị action hiện tại (JUMP/HOVER/FALL)

---

## 🧠 CÔNG NGHỆ & THUẬT TOÁN

### Architecture:
```
Microphone Input
    ↓
Audio Stream (50ms chunks)
    ↓
RMS Volume Calculation
    ↓
Noise Floor Subtraction
    ↓
Moving Average Smoothing
    ↓
Threshold Comparison
    ↓
Game Action (jump/hover/fall)
    ↓
Bird Movement
```

### Key Features:
- **Real-time processing**: Latency ~50-100ms
- **Auto-calibration**: Tự động loại bỏ tiếng ồn nền
- **Smoothing algorithm**: Moving average (5 samples)
- **Dynamic scaling**: Tự động điều chỉnh theo volume max
- **Thread-safe**: Audio processing chạy trên thread riêng

### Signal Processing:
```python
# RMS (Root Mean Square) Volume
rms = sqrt(mean(audio_data²))

# Noise floor removal
volume = max(0, rms - noise_floor)

# Normalization to 0-1
volume = min(1.0, volume / (max_volume * 1.5))

# Smoothing (moving average)
smoothed = mean(last_5_volumes)
```

---

## 🎯 MẸO CHƠI HAY

1. **Tập thở đều**: 
   - Thở ra nhẹ nhàng để giữ chim hover ổn định
   - Đừng thở gấp gáp

2. **Thổi ngắn & mạnh**:
   - Thổi nhanh một cái để jump vừa phải
   - Thổi liên tục = bay cao liên tục

3. **Im lặng chiến thuật**:
   - Ngậm miệng khi muốn chim rơi nhanh qua pipe

4. **Tìm sweet spot**:
   - Mỗi người có volume tự nhiên khác nhau
   - Thử nghiệm để tìm cường độ hơi thoải mái nhất

---

## ⚙️ TÙY CHỈNH

### Điều chỉnh độ nhạy trong `breath_controller.py`:

```python
# Line ~40-42
self.threshold_jump = 0.35      # Giảm = nhạy hơn (dễ jump)
self.threshold_hover_min = 0.15  # Tăng = khó hover hơn
self.threshold_hover_max = 0.35
```

### Điều chỉnh smoothing:

```python
# Line ~17
controller = BreathController(smoothing_window=8)  # Tăng = mượt hơn nhưng chậm hơn
```

---

## 🔧 TROUBLESHOOTING

### ❌ "No microphone found"
→ Kiểm tra Settings → Privacy → Microphone → Bật quyền

### ❌ Chim cứ bay liên tục
→ Môi trường quá ồn, chơi ở chỗ yên tĩnh hơn

### ❌ Chim không phản ứng
→ Thổi/nói to hơn, hoặc giảm threshold_jump xuống 0.25

### ❌ Input bị giật
→ Tăng smoothing_window lên 8-10

---

## 📈 ROADMAP (Sắp có)

- [ ] **Voice commands**: "UP", "DOWN", "STOP"
- [ ] **Machine Learning**: Nhận dạng pattern hơi thở
- [ ] **Multiplayer**: 2 người chơi với 2 micro
- [ ] **Recording mode**: Ghi lại breath pattern
- [ ] **Replay mode**: Xem lại breath pattern
- [ ] **AI training**: Dạy AI dựa trên breath data
- [ ] **Mobile version**: Breath control trên mobile
- [ ] **Difficulty adjustment**: Auto-adjust dựa trên performance

---

## 🎓 HỌC GÌ TỪ PROJECT NÀY?

1. **Audio Signal Processing**: 
   - Real-time audio capture
   - RMS volume calculation
   - Noise reduction
   - Signal smoothing

2. **Threading & Concurrency**:
   - Non-blocking audio input
   - Thread-safe operations
   - Lock mechanisms

3. **Game AI Input**:
   - Converting analog input to discrete actions
   - Threshold-based decision making
   - Input smoothing & debouncing

4. **Human-Computer Interaction**:
   - Natural interface design
   - Breath as input modality
   - Calibration & adaptation

5. **Python Libraries**:
   - Sounddevice for audio
   - NumPy for signal processing
   - Pygame for game development
   - Threading for concurrency

---

## 📞 HỖ TRỢ

Gặp lỗi? Có câu hỏi? 
- Đọc file: `HUONG_DAN_BREATH_CONTROL.md`
- Check console output để debug
- Chạy `TEST_MICROPHONE.bat` để kiểm tra

---

## 🎉 READY TO PLAY!

**Mọi thứ đã sẵn sàng!**

1. ✅ Thư viện đã cài: sounddevice
2. ✅ Code đã fix: Không có lỗi
3. ✅ Files đã tạo: 6 files mới
4. ✅ Hướng dẫn đầy đủ

**Chạy ngay:**
```bash
PLAY_BREATH.bat
```

hoặc

```bash
python breath_game.py
```

**Happy breathing! 🎮🎤🐦**


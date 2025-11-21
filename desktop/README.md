# Hướng Dẫn Sử Dụng Desktop Game

## Cài Đặt

### 1. Cài đặt thư viện
\`\`\`bash
cd desktop
pip install -r requirements.txt
\`\`\`

### 2. Chạy game
\`\`\`bash
python main.py
\`\`\`

## Tính Năng

### ✅ Chơi Offline
- Game chạy hoàn toàn offline
- Điểm được lưu local
- Không cần internet để chơi

### ✅ Sync Điểm Online
- Khi có internet, điểm tự động sync lên server
- Xem bảng xếp hạng toàn cầu
- Điểm chờ sync sẽ được gửi khi có kết nối

### ✅ Thống Kê
- High score cá nhân
- Tổng số game đã chơi
- Số điểm chờ sync

## Build File .exe

### 1. Cài PyInstaller
\`\`\`bash
pip install pyinstaller
\`\`\`

### 2. Build
\`\`\`bash
python build_exe.py
\`\`\`

### 3. Chạy .exe
File .exe sẽ được tạo tại: \`dist/FlappyBird.exe\`

Bạn có thể copy file này sang máy khác và chạy mà không cần cài Python!

## Cấu Trúc File

\`\`\`
desktop/
├── main.py              # Entry point
├── api_client.py        # Kết nối API server
├── local_storage.py     # Lưu trữ local
├── game_logic.py        # Game logic gốc
├── build_exe.py         # Script build .exe
├── requirements.txt     # Dependencies
├── scenes/              # Game scenes
└── assets/              # Game assets
\`\`\`

## Troubleshooting

### Game không kết nối được server
- Kiểm tra internet
- Kiểm tra URL server trong api_client.py
- Game vẫn chạy được offline

### Build .exe lỗi
- Đảm bảo đã cài PyInstaller
- Kiểm tra có file main.py
- Chạy lại: \`python build_exe.py\`

### Điểm không sync
- Kiểm tra internet
- Điểm sẽ được lưu local và sync sau
- Xem pending sync trong stats

# BÁO CÁO PHÂN CÔNG NHIỆM VỤ ĐỒ ÁN PYTHON
## Đề tài: Game Flappy Bird Online & Website Ranking

### 1. Thông tin nhóm
*   **Nhóm:** [Tên Nhóm Của Bạn]
*   **Đề tài:** Xây dựng game Flappy Bird phiên bản Desktop có tính năng Online, Bảng xếp hạng và Website giới thiệu.

### 2. Bảng phân công chi tiết

| STT | Thành viên | Vai trò | Nhiệm vụ chi tiết | File phụ trách | Tỷ lệ |
|:---:|:---:|:---:|:---|:---|:---:|
| 1 | **Hưng** | **Leader / Core Dev** | **1. Quản lý dự án:**<br>- Lên kế hoạch, phân chia task.<br>- Quản lý Source Code (Git/GitHub).<br>**2. Lập trình Core Game:**<br>- Xây dựng khung chương trình (Game Loop).<br>- Xử lý vật lý (Trọng lực, Va chạm).<br>- Logic sinh ống cống (Pipe Spawning). | - `desktop/main.py`<br>- `desktop/scenes/play_scene.py`<br>- `desktop/entities/bird.py`<br>- `desktop/entities/pipe.py` | **100%** |
| 2 | **Bảo** | **Backend / Online Dev** | **1. Hệ thống Online:**<br>- Xây dựng API Client & Server.<br>- Database MongoDB & Sync Score.<br>**2. Tính năng nâng cao:**<br>- Login/Register (Device ID).<br>- Shop & Inventory.<br>- Local Storage & Security. | - `app.py`<br>- `database.py`<br>- `desktop/api_client.py`<br>- `desktop/local_storage.py`<br>- `desktop/scenes/login_scene.py` | **100%** |
| 3 | **Tùng** | **Frontend / UI Dev** | **1. Giao diện & Hiệu ứng:**<br>- Thiết kế UI/UX (Menu, HUD).<br>- Hiệu ứng Visual (Particles).<br>**2. Website:**<br>- Landing Page Premium.<br>- Bảng xếp hạng Realtime. | - `website/index.html`<br>- `website/css/style.css`<br>- `website/js/main.js`<br>- `desktop/scenes/menu_scene.py`<br>- `desktop/scenes/game_over_scene.py` | **100%** |
| 4 | **Thắng** | **Tester / Resource** | **1. Quản lý Tài nguyên:**<br>- Xử lý hình ảnh (Sprite sheets).<br>**2. Kiểm thử (QA):**<br>- Test chức năng & Giao diện.<br>**3. Cân bằng Game:**<br>- Tinh chỉnh thông số độ khó. | - `assets/` (Quản lý)<br>- `desktop/config.py` (Giả định)<br>- `tests/test_game.py` (Test cases) | **90%** |
| 5 | **Duy** | **Doc / Deployment** | **1. Âm thanh (Audio):**<br>- Xử lý SFX & Nhạc nền.<br>**2. Tài liệu:**<br>- Viết README & Báo cáo.<br>**3. Đóng gói:**<br>- Build file .exe. | - `README.md`<br>- `requirements.txt`<br>- `desktop/build_exe.py`<br>- `assets/audio/` | **90%** |

### 3. Kết quả đạt được
*   **Game:** Hoàn thiện 100% tính năng, chạy mượt mà, không lỗi nghiêm trọng.
*   **Online:** Kết nối Server ổn định, bảng xếp hạng cập nhật thời gian thực.
*   **Website:** Giao diện đẹp, hiện đại, đầy đủ thông tin.
*   **Teamwork:** Phối hợp nhịp nhàng, sử dụng Git để quản lý code hiệu quả.

### 4. Tự đánh giá
Tất cả thành viên đều hoàn thành tốt nhiệm vụ được giao, có tinh thần trách nhiệm cao và đóng góp tích cực vào sự thành công của dự án.

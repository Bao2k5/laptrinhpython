# Hướng dẫn Triển khai (Deployment Guide)

## Cách 1: GitHub Pages (Tĩnh - Không lưu điểm chung)
*Phù hợp cho: Web đơn giản, miễn phí, không cần cài đặt database.*
*Hạn chế: Điểm cao chỉ lưu trên máy của người chơi.*

1.  **Upload Code**: Đẩy code của bạn lên GitHub.
2.  **Deploy**: Vào Settings > Pages, chọn nhánh `gh-pages` (hoặc `master` / `root`).
3.  **Chơi**: Truy cập vào link `github.io` của bạn.

---

## Cách 2: Render (Động - Lưu điểm chung)
*Phù hợp cho: Tính năng nhiều người chơi, bảng xếp hạng chung.*
*Yêu cầu: Tài khoản Render và database MongoDB.*

### 1. Chuẩn bị MongoDB
Bạn cần một database đám mây. **MongoDB Atlas** là lựa chọn miễn phí tốt.
1.  Tạo tài khoản tại [MongoDB Atlas](https://www.mongodb.com/atlas).
2.  Tạo một cluster miễn phí (Free Cluster).
3.  Lấy **Connection String** (URI). Nó trông giống như: `mongodb+srv://<user>:<password>@cluster0.mongodb.net/...`

### 2. Triển khai lên Render
1.  Tạo tài khoản tại [Render.com](https://render.com).
2.  Nhấn **New +** và chọn **Web Service**.
3.  Kết nối với kho code GitHub của bạn.
4.  **Cài đặt (Settings)**:
    *   **Runtime**: Python 3
    *   **Build Command**: `python build.py`
    *   **Start Command**: `gunicorn app:app`
5.  **Biến môi trường (Environment Variables)** (Quan trọng!):
    *   Key: `MONGO_URI`
    *   Value: (Dán Connection String của MongoDB vào đây)
6.  Nhấn **Create Web Service**.

### 3. Chơi thôi!
Render sẽ cấp cho bạn một đường link (ví dụ: `https://flappy-bird.onrender.com`).
Mọi người chơi trên link này sẽ cùng chia sẻ bảng xếp hạng High Score!

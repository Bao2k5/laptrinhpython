@echo off
chcp 65001 >nul
cls
echo.
echo ═══════════════════════════════════════════════════════════
echo                 GIẢI PHÁP TRIỆT ĐỂ - SETUP GAME
echo ═══════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

echo [1/5] Kiểm tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ PYTHON CHƯA CÀI ĐẶT!
    echo.
    echo Vui lòng cài Python tại: https://www.python.org/downloads/
    echo Sau đó chạy lại script này
    pause
    exit /b 1
)
echo ✅ Python đã cài đặt
echo.

echo [2/5] Cài đặt các module cần thiết...
echo Installing pygame...
pip install pygame --quiet
if errorlevel 1 (
    echo ⚠️  Lỗi cài pygame, thử lại...
    pip install pygame
)

echo Installing neat-python...
pip install neat-python --quiet
if errorlevel 1 (
    echo ⚠️  Lỗi cài neat-python, thử lại...
    pip install neat-python
)
echo ✅ Đã cài đặt pygame và neat-python
echo.

echo [3/5] Kiểm tra file cần thiết...
if not exist "imgs\" (
    echo ❌ Thư mục imgs/ không tồn tại!
    echo Vui lòng tạo thư mục imgs/ và thêm các file ảnh
    pause
    exit /b 1
)

if not exist "imgs\bird1.png" (
    echo ❌ Thiếu file: imgs\bird1.png
    echo Vui lòng thêm các file ảnh vào thư mục imgs/
    pause
    exit /b 1
)

if not exist "config-feedforward.txt" (
    echo ❌ Thiếu file: config-feedforward.txt
    echo Vui lòng đảm bảo có file config
    pause
    exit /b 1
)

if not exist "menu.py" (
    echo ⚠️  menu.py không tồn tại, tạo menu đơn giản...
    copy simple_menu.py menu.py >nul
    echo ✅ Đã tạo menu.py
) else (
    echo ✅ menu.py đã tồn tại
)

echo ✅ Tất cả file cần thiết đã sẵn sàng
echo.

echo [4/5] Chọn phiên bản game...
echo.
echo Có 3 phiên bản:
echo   1. game_fixed.py     - KHUYẾN NGHỊ (Đã fix lỗi, không cần DB)
echo   2. game.py           - Phiên bản gốc (Cần MongoDB)
echo   3. flappy_game_minimal.py - Phiên bản tối giản
echo.
set /p choice="Chọn (1/2/3) [Mặc định: 1]: "
if "%choice%"=="" set choice=1

if "%choice%"=="1" (
    set gamefile=game_fixed.py
    echo ✅ Đã chọn: game_fixed.py
) else if "%choice%"=="2" (
    set gamefile=game.py
    echo ✅ Đã chọn: game.py
    echo ⚠️  Lưu ý: Cần cài MongoDB nếu dùng phiên bản này
) else if "%choice%"=="3" (
    set gamefile=flappy_game_minimal.py
    echo ✅ Đã chọn: flappy_game_minimal.py
) else (
    echo ❌ Lựa chọn không hợp lệ!
    pause
    exit /b 1
)
echo.

echo [5/5] Khởi động game...
echo.
echo ════════════════════════════════════════════════════════════
echo                    ĐANG KHỞI ĐỘNG GAME...
echo ════════════════════════════════════════════════════════════
echo.

python %gamefile%

if errorlevel 1 (
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo                        CÓ LỖI XẢY RA!
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo Vui lòng:
    echo 1. Đọc file HUONG_DAN_TRIET_DE.txt
    echo 2. Chạy: python fix_errors.py để kiểm tra lỗi
    echo 3. Chạy: python test_game.py để test
    echo.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════
echo                    GAME ĐÃ ĐÓNG
echo ═══════════════════════════════════════════════════════════
echo.
pause


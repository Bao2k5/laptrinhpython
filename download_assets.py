"""
Auto Download Assets cho Future Development
Tai tu cac nguon mien phi va luu vao future_assets/
"""

import os
import urllib.request
import sys

def download_file(url, filepath):
    """Download file từ URL"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        print(f"Đang tải: {os.path.basename(filepath)}...")
        urllib.request.urlretrieve(url, filepath)
        print(f"✓ Đã tải: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"✗ Lỗi tải {os.path.basename(filepath)}: {e}")
        return False

def main():
    base_dir = "future_assets"

    # Danh sách các assets cần tải từ Flappy Bird sprites
    # Đã loại bỏ các file trùng lặp
    assets = {
        # Backgrounds - đã loại bỏ bg_sunset (trùng bg_day)
        "backgrounds/bg_cloudy.png": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/background-night.png",
        "backgrounds/bg_day.png": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/background-day.png",
        
        # Buttons
        "buttons/play_button.png": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/message.png",
        "buttons/pause_button.png": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/gameover.png",
        
        # Characters - 7 loại chim khác nhau (đã loại bỏ trùng lặp)
        # bird_blue, bird_red, bird_yellow là 3 màu chính
        "characters/bird_red.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/redbird-upflap.png",
        "characters/bird_blue2.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/bluebird-upflap.png",
        
        # Thêm các animation frames cho chim (midflap)
        "characters/bird_blue_1.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/bluebird-midflap.png",
        "characters/bird_red_mid.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/redbird-midflap.png",
        "characters/bird_yellow_mid.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/yellowbird-midflap.png",
        
        # Numbers for score display
        "effects/number_1.png": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/1.png",
        "effects/number_2.png": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/2.png",
        "effects/number_3.png": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/3.png",
        "effects/number_4.png": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/4.png",
        "effects/number_5.png": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/5.png",
        "effects/number_6.png": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/6.png",
        "effects/number_7.png": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/7.png",
        "effects/number_8.png": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/8.png",
        "effects/number_9.png": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/9.png",
        
        # Thêm các pipes màu khác - đã loại bỏ pipe_yellow (trùng pipe_red)
        "backgrounds/pipe_blue.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/pipe-green.png",
        
        # Sounds
        "sounds/die.wav": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/audio/die.wav",
        "sounds/hit.wav": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/audio/hit.wav",
        "sounds/point.wav": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/audio/point.wav",
        "sounds/swoosh.wav": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/audio/swoosh.wav",
        "sounds/wing.wav": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/audio/wing.wav",
    }

    print("=" * 60)
    print("BẮT ĐẦU TẢI CÁC ASSETS CHO FLAPPY BIRD")
    print("=" * 60)

    success_count = 0
    fail_count = 0
    skip_count = 0

    for relative_path, url in assets.items():
        filepath = os.path.join(base_dir, relative_path)

        # Kiểm tra file đã tồn tại chưa
        if os.path.exists(filepath):
            print(f"→ Đã có: {relative_path}")
            skip_count += 1
            continue

        # Tải file
        if download_file(url, filepath):
            success_count += 1
        else:
            fail_count += 1

    print("\n" + "=" * 60)
    print("KẾT QUẢ TẢI ASSETS")
    print("=" * 60)
    print(f"✓ Tải thành công: {success_count}")
    print(f"→ Đã có sẵn: {skip_count}")
    print(f"✗ Thất bại: {fail_count}")
    print(f"Tổng cộng: {success_count + skip_count + fail_count}")

    if fail_count > 0:
        print("\n⚠ Một số file không tải được. Vui lòng kiểm tra kết nối mạng.")
        return 1
    else:
        print("\n✓ Đã hoàn thành tải tất cả assets!")
        return 0

if __name__ == "__main__":
    sys.exit(main())

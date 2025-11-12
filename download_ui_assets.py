"""
Download UI Assets cho Flappy Bird
Tai buttons, panels, icons tu nguon mien phi
"""

import os
import urllib.request
import sys

def download_file(url, filepath):
    """Download file tu URL"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        print(f"Dang tai: {os.path.basename(filepath)}...")
        urllib.request.urlretrieve(url, filepath)
        print(f"Da tai: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"Loi tai {os.path.basename(filepath)}: {e}")
        return False

def main():
    base_dir = "future_assets"

    # Danh sach UI assets tu Flappy Bird official va cac nguon free
    ui_assets = {
        # Buttons
        "ui/btn_play.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/message.png",
        "ui/btn_pause.png": "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/base.png",
        "ui/btn_resume.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/bluebird-midflap.png",
        "ui/btn_restart.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/redbird-midflap.png",
        "ui/btn_menu.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/yellowbird-midflap.png",
        "ui/btn_settings.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/bluebird-upflap.png",

        # Score numbers (already have 0-9 in effects, but adding here for UI)
        "ui/number_0.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/0.png",
        "ui/number_1.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/1.png",
        "ui/number_2.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/2.png",
        "ui/number_3.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/3.png",
        "ui/number_4.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/4.png",
        "ui/number_5.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/5.png",
        "ui/number_6.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/6.png",
        "ui/number_7.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/7.png",
        "ui/number_8.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/8.png",
        "ui/number_9.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/9.png",

        # Panels and screens
        "ui/panel_game_over.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/gameover.png",
        "ui/panel_message.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/message.png",

        # Medal/achievements icons (using bird sprites as placeholders)
        "ui/medal_bronze.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/yellowbird-downflap.png",
        "ui/medal_silver.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/bluebird-downflap.png",
        "ui/medal_gold.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/redbird-downflap.png",

        # Extra sprites for UI
        "ui/base.png": "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/base.png",
    }

    print("=" * 60)
    print("BAT DAU TAI UI ASSETS CHO FLAPPY BIRD")
    print("=" * 60)

    success_count = 0
    fail_count = 0
    skip_count = 0

    for relative_path, url in ui_assets.items():
        filepath = os.path.join(base_dir, relative_path)

        # Kiem tra file da ton tai chua
        if os.path.exists(filepath):
            print(f"Da co: {relative_path}")
            skip_count += 1
            continue

        # Tai file
        if download_file(url, filepath):
            success_count += 1
        else:
            fail_count += 1

    print("\n" + "=" * 60)
    print("KET QUA TAI UI ASSETS")
    print("=" * 60)
    print(f"Tai thanh cong: {success_count}")
    print(f"Da co san: {skip_count}")
    print(f"That bai: {fail_count}")
    print(f"Tong cong: {success_count + skip_count + fail_count}")

    if fail_count > 0:
        print("\nMot so file khong tai duoc. Vui long kiem tra ket noi mang.")
        return 1
    else:
        print("\nDa hoan thanh tai tat ca UI assets!")
        return 0

if __name__ == "__main__":
    sys.exit(main())


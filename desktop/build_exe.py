"""
Build script để tạo file .exe từ game
Sử dụng PyInstaller
"""

import PyInstaller.__main__
import os
import sys

def build_exe():
    """Build game thành file .exe"""
    
    print("="*50)
    print("BUILDING FLAPPY BIRD .EXE")
    print("="*50)
    
    # Xác định đường dẫn main.py
    main_path = "main.py"
    if not os.path.exists(main_path):
        # Thử tìm trong thư mục desktop nếu chạy từ root
        if os.path.exists("desktop/main.py"):
            main_path = "desktop/main.py"
        else:
            print(f"[ERROR] {main_path} not found!")
            sys.exit(1)
    
    # PyInstaller arguments
    args = [
        main_path,
        '--name=FlappyBird_v2.4',
        '--onefile',  # Tạo 1 file .exe duy nhất
        '--windowed',  # Không hiện console window
        '--add-data=scenes;scenes',  # Thêm scenes folder
        '--clean',  # Clean build cache
        '--noconfirm',  # Không hỏi confirm
    ]
    
    # Thêm assets nếu có
    if os.path.exists("assets"):
        args.append('--add-data=assets;assets')
    
    # Thêm icon nếu có
    if os.path.exists("assets/icon.ico"):
        args.append('--icon=assets/icon.ico')
    
    print("\nBuilding with PyInstaller...")
    print(f"Arguments: {' '.join(args)}\n")
    
    try:
        PyInstaller.__main__.run(args)
        print("\n" + "="*50)
        print("[SUCCESS] BUILD SUCCESSFUL!")
        print("="*50)
        print(f"\nFile .exe được tạo tại: dist/FlappyBird.exe")
        print("Bạn có thể chạy file này trên bất kỳ máy Windows nào!")
    except Exception as e:
        print(f"\n[ERROR] Build failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_exe()

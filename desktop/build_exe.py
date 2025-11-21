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
    
    # Kiểm tra file main.py tồn tại
    if not os.path.exists("main.py"):
        print("✗ Error: main.py not found!")
        sys.exit(1)
    
    # PyInstaller arguments
    args = [
        'main.py',
        '--name=FlappyBird',
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
        print("✓ BUILD SUCCESSFUL!")
        print("="*50)
        print(f"\nFile .exe được tạo tại: dist/FlappyBird.exe")
        print("Bạn có thể chạy file này trên bất kỳ máy Windows nào!")
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_exe()

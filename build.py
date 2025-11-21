import os
import sys

def build():
    print("--- Bắt đầu cài đặt và build game ---")
    
    # 1. Cài đặt thư viện
    print("1. Đang cài đặt thư viện từ requirements.txt...")
    exit_code = os.system("pip install -r requirements.txt")
    if exit_code != 0:
        print("Lỗi khi cài đặt thư viện!")
        sys.exit(1)

    # 2. Build game bằng pygbag
    print("2. Đang build game sang Web (WASM)...")
    # --build: build xong thoát
    exit_code = os.system("python -m pygbag --build main.py")
    if exit_code != 0:
        print("Lỗi khi build game!")
        sys.exit(1)
        
    print("--- Hoàn tất! ---")

if __name__ == "__main__":
    build()

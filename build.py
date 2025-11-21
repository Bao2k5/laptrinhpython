import os
import sys

def build():
    print("--- Bắt đầu cài đặt thư viện ---")
    
    # Cài đặt thư viện
    print("Đang cài đặt thư viện từ requirements.txt...")
    exit_code = os.system("pip install -r requirements.txt")
    if exit_code != 0:
        print("Lỗi khi cài đặt thư viện!")
        sys.exit(1)
        
    print("--- Hoàn tất! ---")
    print("Lưu ý: File game đã được build sẵn trong thư mục build/web")

if __name__ == "__main__":
    build()


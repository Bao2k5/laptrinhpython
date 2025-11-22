import os
import requests

# Cấu hình thư mục lưu
DOWNLOAD_DIR = "assets/downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Danh sách các URL assets xịn (từ samuelcust/flappy-bird-assets)
BASE_URL = "https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites"

ASSETS = {
    "background-day.png": f"{BASE_URL}/background-day.png",
    "background-night.png": f"{BASE_URL}/background-night.png",
    "base.png": f"{BASE_URL}/base.png",
    "bluebird-downflap.png": f"{BASE_URL}/bluebird-downflap.png",
    "bluebird-midflap.png": f"{BASE_URL}/bluebird-midflap.png",
    "bluebird-upflap.png": f"{BASE_URL}/bluebird-upflap.png",
    "redbird-downflap.png": f"{BASE_URL}/redbird-downflap.png",
    "redbird-midflap.png": f"{BASE_URL}/redbird-midflap.png",
    "redbird-upflap.png": f"{BASE_URL}/redbird-upflap.png",
    "yellowbird-downflap.png": f"{BASE_URL}/yellowbird-downflap.png",
    "yellowbird-midflap.png": f"{BASE_URL}/yellowbird-midflap.png",
    "yellowbird-upflap.png": f"{BASE_URL}/yellowbird-upflap.png",
    "pipe-green.png": f"{BASE_URL}/pipe-green.png",
    "pipe-red.png": f"{BASE_URL}/pipe-red.png",
    "message.png": f"{BASE_URL}/message.png",
    "gameover.png": f"{BASE_URL}/gameover.png"
}

def download_file(url, filename):
    print(f"Downloading {filename}...", end=" ")
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        file_path = os.path.join(DOWNLOAD_DIR, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print("✅ Done!")
    except Exception as e:
        print(f"❌ Failed: {e}")

def main():
    print(f"🚀 Starting Asset Downloader...")
    print(f"📂 Saving to: {os.path.abspath(DOWNLOAD_DIR)}\n")
    
    count = 0
    for filename, url in ASSETS.items():
        download_file(url, filename)
        count += 1
        
    print(f"\n✨ Completed! Downloaded {count} files.")
    print("👉 Check the 'assets/downloads' folder.")

if __name__ == "__main__":
    main()

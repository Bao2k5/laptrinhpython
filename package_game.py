import zipfile
import os
import shutil

def package_game():
    # Tên file zip output
    zip_name = "FlappyBird_v2.3.zip"
    
    # File exe nguồn
    exe_path = "dist/FlappyBird_v2.3.exe"
    
    if not os.path.exists(exe_path):
        print(f"[ERROR] {exe_path} not found! Please build the game first.")
        return

    print(f"Creating {zip_name}...")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add exe
        print(f"Adding {exe_path}...")
        zipf.write(exe_path, "FlappyBird.exe")
        
        # Add assets folder if exists
        if os.path.exists("assets"):
            print("Adding assets folder...")
            for root, dirs, files in os.walk("assets"):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, file_path)
        
        # Add README if exists
        if os.path.exists("README.md"):
            print("Adding README.md...")
            zipf.write("README.md", "README.md")

    print(f"\n[SUCCESS] Created {zip_name}")
    print(f"Location: {os.path.abspath(zip_name)}")

if __name__ == "__main__":
    package_game()

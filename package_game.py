import zipfile
import os
import shutil

def package_game():
    # Tên file zip output
    zip_name = "FlappyBird_v2.4.zip"
    
    # File exe nguồn
    # Note: build_exe.py creates it in dist/FlappyBird_v2.4.exe
    exe_path = "dist/FlappyBird_v2.4.exe"
    
    if not os.path.exists(exe_path):
        # Fallback check in desktop/dist if run from root
        if os.path.exists("desktop/dist/FlappyBird_v2.4.exe"):
            exe_path = "desktop/dist/FlappyBird_v2.4.exe"
        else:
            print(f"[ERROR] {exe_path} not found! Please build the game first.")
            return

    print(f"Creating {zip_name}...")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add exe
        print(f"Adding {exe_path}...")
        zipf.write(exe_path, "FlappyBird_v2.4.exe")
        
        # Assets are now bundled inside the exe via PyInstaller --add-data
        # So we don't need to distribute the assets folder separately anymore!
        
        # Add README if exists
        
        # Add README if exists
        if os.path.exists("README.md"):
            print("Adding README.md...")
            zipf.write("README.md", "README.md")

    print(f"\n[SUCCESS] Created {zip_name}")
    print(f"Location: {os.path.abspath(zip_name)}")

if __name__ == "__main__":
    package_game()

import subprocess
import sys
import os

print("="*50)
print("RENDER BUILD SCRIPT")
print("="*50)

# Step 1: Install dependencies
print("\n--- Step 1: Installing dependencies ---")
try:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        check=True
    )
    print("✓ Dependencies installed successfully")
except subprocess.CalledProcessError as e:
    print(f"✗ Failed to install dependencies: {e}")
    sys.exit(1)

# Step 2: Build game with pygbag
print("\n--- Step 2: Building game with pygbag ---")
print("This will create build/web directory with index.html and game files")
try:
    # Run pygbag to build the game
    subprocess.run(
        [sys.executable, "-m", "pygbag", "--build", "main.py"],
        check=True
    )
    print("✓ Game built successfully with pygbag")
except subprocess.CalledProcessError as e:
    print(f"✗ Failed to build game: {e}")
    sys.exit(1)

# Step 3: Verify build output
print("\n--- Step 3: Verifying build output ---")
build_dir = "build/web"
required_files = ["index.html", "laptrinhpy.apk"]

if os.path.exists(build_dir):
    files = os.listdir(build_dir)
    print(f"Files in {build_dir}: {files}")
    
    missing_files = [f for f in required_files if f not in files]
    if missing_files:
        print(f"✗ Missing required files: {missing_files}")
        sys.exit(1)
    else:
        print("✓ All required files present")
else:
    print(f"✗ Build directory {build_dir} not found")
    sys.exit(1)

print("\n" + "="*50)
print("BUILD COMPLETE!")
print("="*50)

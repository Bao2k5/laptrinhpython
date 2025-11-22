"""Simple asset check"""
import os
import sys
from pathlib import Path

desktop_dir = Path(__file__).parent
sys.path.insert(0, str(desktop_dir))

from game_utils import asset_path

print("Checking assets...")
assets = [
    'assets/bluebird-upflap.png',
    'assets/bluebird-midflap.png', 
    'assets/bluebird-downflap.png',
    'assets/redbird-upflap.png',
    'assets/redbird-midflap.png',
    'assets/redbird-downflap.png',
    'assets/background-day.png',
    'assets/background-night.png',
    'assets/pipe-green.png',
    'assets/pipe-red.png'
]

for asset in assets:
    path = asset_path(*asset.split('/'))
    exists = "YES" if os.path.exists(path) else "NO"
    print(f"{exists}: {asset}")

print("\nDone!")

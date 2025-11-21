"""
Utility functions for desktop game
"""
import os
import sys

def in_browser():
    """Check if running in browser (always False for desktop)"""
    return False

def asset_path(relative_path):
    """Get absolute path to asset, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

"""
Utility functions for desktop game
"""
import os
import sys
import pygame

def in_browser():
    """Check if running in browser (always False for desktop)"""
    return False

def asset_path(*args):
    """Get absolute path to asset, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, *args)

def load_sound(path):
    """Load sound safely"""
    try:
        return pygame.mixer.Sound(asset_path(path))
    except Exception as e:
        print(f"Warning: Could not load sound {path}: {e}")
        return None

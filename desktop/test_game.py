"""
Automated Game Testing Script
Tests all major game features and reports any issues
"""

import pygame
import sys
import os
import asyncio
from pathlib import Path

# Add desktop directory to path
desktop_dir = Path(__file__).parent
sys.path.insert(0, str(desktop_dir))

from local_storage import LocalStorage
from scenes.shop_scene import ShopScene
from scenes.play_scene import PlayScene
from game_utils import asset_path

class GameTester:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 600))
        pygame.display.set_caption("Game Testing")
        self.storage = LocalStorage()
        self.results = []
        
    def test_assets_exist(self):
        """Test that all required assets exist"""
        print("\n=== Testing Asset Files ===")
        required_assets = [
            # Bird sprites
            'assets/bird-up.png', 'assets/bird-mid.png', 'assets/bird-down.png',
            'assets/bluebird-upflap.png', 'assets/bluebird-midflap.png', 'assets/bluebird-downflap.png',
            'assets/redbird-upflap.png', 'assets/redbird-midflap.png', 'assets/redbird-downflap.png',
            # Backgrounds
            'assets/background-day.png', 'assets/background-night.png',
            # Pipes
            'assets/pipe-green.png', 'assets/pipe-red.png',
            # UI
            'assets/base.png', 'assets/coin.png',
            # Sounds
            'assets/flap.wav', 'assets/hit.wav'
        ]
        
        missing = []
        for asset in required_assets:
            path = asset_path(*asset.split('/'))
            if not os.path.exists(path):
                missing.append(asset)
                print(f"  [FAIL] MISSING: {asset}")
            else:
                print(f"  [PASS] Found: {asset}")
        
        if missing:
            self.results.append(f"FAIL: {len(missing)} assets missing")
            return False
        else:
            self.results.append("PASS: All assets found")
            return True
    
    def test_storage(self):
        """Test local storage functionality"""
        print("\n=== Testing Local Storage ===")
        try:
            # Test coin operations
            initial_coins = self.storage.get_coins()
            self.storage.add_coins(50)
            if self.storage.get_coins() != initial_coins + 50:
                raise Exception("Add coins failed")
            print("  [PASS] Add coins works")
            
            self.storage.spend_coins(25)
            if self.storage.get_coins() != initial_coins + 25:
                raise Exception("Spend coins failed")
            print("  [PASS] Spend coins works")
            
            # Test skin operations
            self.storage.unlock_skin("blue")
            inventory = self.storage.get_inventory()
            if "blue" not in inventory:
                raise Exception("Unlock skin failed")
            print("  [PASS] Unlock skin works")
            
            self.storage.set_skin("blue")
            if self.storage.get_current_skin() != "blue":
                raise Exception("Set skin failed")
            print("  [PASS] Set current skin works")
            
            # Reset to default
            self.storage.set_skin("yellow")
            
            self.results.append("PASS: Storage operations work")
            return True
            
        except Exception as e:
            print(f"  [FAIL] Storage test failed: {e}")
            self.results.append(f"FAIL: Storage - {e}")
            return False
    
    def test_shop_scene_init(self):
        """Test that ShopScene initializes without errors"""
        print("\n=== Testing Shop Scene Initialization ===")
        try:
            shop = ShopScene(self.screen, "test_player", storage=self.storage)
            print("  [PASS] ShopScene initialized successfully")
            print(f"  [INFO] Found {len(shop.birds)} bird variants")
            print(f"  [INFO] Found {len(shop.items)} shop items")
            self.results.append("PASS: ShopScene initialization")
            return True
        except Exception as e:
            print(f"  [FAIL] ShopScene init failed: {e}")
            self.results.append(f"FAIL: ShopScene - {e}")
            return False
    
    def test_play_scene_init(self):
        """Test that PlayScene initializes for each skin"""
        print("\n=== Testing Play Scene Initialization ===")
        skins = ["yellow", "blue", "red"]
        
        for skin in skins:
            try:
                self.storage.set_skin(skin)
                play = PlayScene(self.screen, "test_player", storage=self.storage)
                print(f"  [PASS] PlayScene initialized with {skin} skin")
                print(f"    - Bird frames: {len(play.bird_frames)}")
                print(f"    - Current skin: {play.current_skin}")
            except Exception as e:
                print(f"  [FAIL] PlayScene init failed for {skin}: {e}")
                self.results.append(f"FAIL: PlayScene {skin} - {e}")
                return False
        
        # Reset to default
        self.storage.set_skin("yellow")
        self.results.append("PASS: PlayScene initialization for all skins")
        return True
    
    def run_tests(self):
        """Run all tests"""
        print("="*60)
        print("FLAPPY BIRD - COMPREHENSIVE GAME TEST")
        print("="*60)
        
        tests = [
            self.test_assets_exist,
            self.test_storage,
            self.test_shop_scene_init,
            self.test_play_scene_init
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            if test():
                passed += 1
            else:
                failed += 1
        
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        for result in self.results:
            print(f"  {result}")
        print(f"\nTotal: {passed} passed, {failed} failed")
        print("="*60)
        
        pygame.quit()
        return failed == 0

if __name__ == "__main__":
    tester = GameTester()
    success = tester.run_tests()
    sys.exit(0 if success else 1)

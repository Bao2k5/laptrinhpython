"""
Desktop Flappy Bird Game
Chơi offline, sync điểm online khi có internet
"""

import sys
import asyncio
import pygame
from api_client import APIClient
from local_storage import LocalStorage

# Import scenes
from scenes.login_scene import LoginScene
from scenes.register_scene import RegisterScene
from scenes.menu_scene import MenuScene
from scenes.play_scene import PlayScene
from scenes.scores_scene import ScoresScene
from scenes.gameover_scene import GameOverScene
from scenes.train_scene import TrainScene
from scenes.shop_scene import ShopScene


class DesktopGame:
    """Main game class với offline/online support"""
    
    def __init__(self):
        pygame.init()
        
        # Screen setup
        self.WIDTH, self.HEIGHT = 500, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Flappy Bird - Desktop Edition")
        
        # Clock
        self.clock = pygame.time.Clock()
        
        # API và Storage
        self.api = APIClient()
        self.storage = LocalStorage()
        
        # Scene management
        self.current_scene = "login"
        self.scene_data = {"player": None}
        
        # Check connection at startup
        self.check_and_sync()
    
    def check_and_sync(self):
        """Kiểm tra kết nối và sync điểm chờ"""
        print("\n" + "="*50)
        print("FLAPPY BIRD - DESKTOP EDITION")
        print("="*50)
        
        if self.api.check_connection():
            print("✓ Online mode - Connected to server")
            
            # Sync pending scores
            pending = self.storage.get_pending_sync()
            if pending:
                print(f"\nSyncing {len(pending)} pending scores...")
                synced = 0
                device_id = self.storage.get_device_id()
                for i, item in enumerate(pending):
                    if self.api.submit_score(item["username"], item["score"], device_id):
                        self.storage.remove_synced_score(i - synced)
                        synced += 1
                        print(f"  ✓ Synced {item['username']}: {item['score']}")
                
                if synced > 0:
                    print(f"✓ Successfully synced {synced} scores!")
        else:
            print("⚠ Offline mode - Scores will be saved locally")
        
        # Show stats
        stats = self.storage.get_stats()
        print(f"\nYour Stats:")
        print(f"  High Score: {stats['high_score']}")
        print(f"  Total Games: {stats['total_games']}")
        if stats['pending_sync'] > 0:
            print(f"  Pending Sync: {stats['pending_sync']} scores")
        print("="*50 + "\n")
    
    def goto(self, scene_name, **kwargs):
        """Chuyển scene"""
        # Preserve player if not provided
        if "player" not in kwargs:
            kwargs["player"] = self.scene_data.get("player")
        
        self.scene_data = kwargs
        self.current_scene = scene_name
    
    async def handle_game_over(self, player, score):
        """Xử lý khi game over - lưu điểm và sync"""
        username = player if player else self.storage.get_username()
        
        # Increment game count
        self.storage.increment_games()
        
        # Check if new high score
        is_new_record = self.storage.update_high_score(score)
        if is_new_record:
            print(f"\n🎉 NEW HIGH SCORE: {score}!")
        
        # Try to sync online
        if self.api.check_connection():
            device_id = self.storage.get_device_id()
            if self.api.submit_score(username, score, device_id):
                print(f"✓ Score synced to server: {score}")
            else:
                print("⚠ Failed to sync - saving for later")
                self.storage.add_pending_sync(username, score)
        else:
            print(f"⚠ Offline - Score saved locally: {score}")
            self.storage.add_pending_sync(username, score)
    
    async def run(self):
        """Main game loop"""
        try:
            while True:
                player = self.scene_data.get("player")
                
                if self.current_scene == "login":
                    next_scene, data = await LoginScene(self.screen).run()
                    self.goto(next_scene, **data)
                
                elif self.current_scene == "register":
                    next_scene, data = await RegisterScene(self.screen).run()
                    self.goto(next_scene, **data)
                
                elif self.current_scene == "menu":
                    next_scene, data = await MenuScene(self.screen, player).run()
                    self.goto(next_scene, **data)
                
                elif self.current_scene == "play":
                    # Truyền API và Storage vào PlayScene
                    scene = PlayScene(self.screen, player, api=self.api, storage=self.storage)
                    next_scene, data = await scene.run()
                    
                    # If game over, handle score
                    if next_scene == "gameover" and "score" in data:
                        await self.handle_game_over(player, data["score"])
                    
                    self.goto(next_scene, **data)
                
                elif self.current_scene == "scores":
                    next_scene, data = await ScoresScene(self.screen, player, api=self.api, storage=self.storage).run()
                    self.goto(next_scene, **data)
                
                elif self.current_scene == "shop":
                    next_scene, data = await ShopScene(self.screen, player, api=self.api, storage=self.storage).run()
                    self.goto(next_scene, **data)
                
                elif self.current_scene == "gameover":
                    score = self.scene_data.get("score", 0)
                    next_scene, data = await GameOverScene(self.screen, player, score).run()
                    self.goto(next_scene, **data)
                
                elif self.current_scene == "train":
                    next_scene, data = await TrainScene(self.screen).run()
                    self.goto(next_scene, **data)
                
                else:
                    print(f"Unknown scene: {self.current_scene}")
                    break
        
        except Exception as e:
            import traceback
            err_msg = traceback.format_exc()
            print(err_msg)
            
            # Show error on screen
            font = pygame.font.SysFont("Arial", 14)
            while True:
                self.screen.fill((0, 0, 0))
                y = 10
                for line in err_msg.split('\n'):
                    txt = font.render(line, True, (255, 0, 0))
                    self.screen.blit(txt, (10, y))
                    y += 20
                pygame.display.update()
                await asyncio.sleep(0)
        
        finally:
            pygame.quit()
            sys.exit()


async def main():
    """Entry point"""
    game = DesktopGame()
    await game.run()


if __name__ == "__main__":
    # Run game
    asyncio.run(main())

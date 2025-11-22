import pygame
import sys
import asyncio
from local_storage import LocalStorage

WIDTH, HEIGHT = 500, 600

class ScoresScene:
    def __init__(self, screen, player_name, api=None, storage=None):
        self.screen = screen
        self.player_name = player_name
        self.api = api
        self.storage = storage or LocalStorage()
        self.font_big = pygame.font.Font(None, 60)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 30)

    async def run(self):
        back_rect = pygame.Rect(150, 520, 200, 45)
        
        # Get local stats
        stats = self.storage.get_stats()
        high_score = stats.get("high_score", 0)
        total_games = stats.get("total_games", 0)
        coins = stats.get("coins", 0)
        
        # Try to get online leaderboard
        online_scores = []
        if self.api:
            try:
                online_scores = self.api.get_leaderboard(10)
            except:
                pass

        while True:
            await asyncio.sleep(0)
            self.screen.fill((20, 20, 60))

            # Title
            title = self.font_big.render("STATISTICS", True, (255, 255, 0))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))

            # Local Stats Section
            y = 120
            
            # Player name
            player_txt = self.font_medium.render(f"Player: {self.player_name}", True, (100, 200, 255))
            self.screen.blit(player_txt, (50, y))
            y += 60
            
            # High Score
            score_txt = self.font_small.render(f"High Score: {high_score}", True, (255, 255, 255))
            self.screen.blit(score_txt, (50, y))
            y += 40
            
            # Total Games
            games_txt = self.font_small.render(f"Games Played: {total_games}", True, (255, 255, 255))
            self.screen.blit(games_txt, (50, y))
            y += 40
            
            # Coins
            coins_txt = self.font_small.render(f"Total Coins: {coins}", True, (255, 215, 0))
            self.screen.blit(coins_txt, (50, y))
            y += 60

            # Online Leaderboard Section (if available)
            if online_scores:
                leaderboard_title = self.font_medium.render("Online Top 5", True, (0, 255, 100))
                self.screen.blit(leaderboard_title, (50, y))
                y += 45
                
                for i, score_data in enumerate(online_scores[:5], 1):
                    try:
                        username = score_data.get("username", "Unknown")
                        score_val = score_data.get("score", 0)
                    except:
                        username = score_data.username if hasattr(score_data, 'username') else "Unknown"
                        score_val = score_data.score if hasattr(score_data, 'score') else 0
                    
                    rank_txt = self.font_small.render(
                        f"{i}. {username}: {score_val}",
                        True, (200, 200, 200)
                    )
                    self.screen.blit(rank_txt, (70, y))
                    y += 35
            else:
                # Offline message
                offline_txt = self.font_small.render("Offline - No online scores", True, (150, 150, 150))
                self.screen.blit(offline_txt, (50, y))

            # Back Button
            pygame.draw.rect(self.screen, (0, 180, 255), back_rect, border_radius=10)
            back_txt = self.font_medium.render("BACK", True, (255, 255, 255))
            self.screen.blit(back_txt, (back_rect.x + 60, back_rect.y + 5))

            pygame.display.update()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if back_rect.collidepoint(e.pos):
                        return "menu", {"player": self.player_name}
                        
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        return "menu", {"player": self.player_name}

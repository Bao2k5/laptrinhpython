import pygame
import sys
import asyncio
import json
from utils import in_browser, asset_path

WIDTH, HEIGHT = 500, 600

class ScoresScene:
    def __init__(self, screen, player_name):
        self.screen = screen
        self.player_name = player_name
        self.font_big = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 35)

    async def run(self):
        back_rect = pygame.Rect(150, 520, 200, 45)
        
        # Fetch scores once
        scores = []
        if in_browser():
            try:
                from js import fetch, JSON
                response = await fetch('/api/scores')
                text = await response.text()
                scores = JSON.parse(text)
            except Exception as e:
                print(f"Error fetching scores: {e}")
                scores = []
        else:
            try:
                from database import get_top_scores
                scores = get_top_scores()
            except Exception:
                scores = []

        while True:
            await asyncio.sleep(0)
            self.screen.fill((20, 20, 60))

            title = self.font_big.render("TOP SCORES", True, (255, 255, 0))
            self.screen.blit(title, (120, 40))

            y = 130
            rank = 1

            for s in scores:
                # Handle both dict (python) and JS object (browser) if needed, 
                # but JSON.parse usually returns dict-like in python-wasm bridge or we need to access attributes.
                # If using pygbag, it might be a JS proxy.
                # Safest is to try dict access, if fail try attr access.
                try:
                    username = s.get("username", "Unknown")
                    score_val = s.get("score", 0)
                except:
                    # If it's a JS object proxy
                    username = s.username if hasattr(s, 'username') else "Unknown"
                    score_val = s.score if hasattr(s, 'score') else 0

                txt = self.font_small.render(
                    f"{rank}. {username} — {score_val}",
                    True, (255, 255, 255)
                )
                self.screen.blit(txt, (80, y))
                y += 40
                rank += 1

            pygame.draw.rect(self.screen, (0, 180, 255), back_rect)
            self.screen.blit(
                self.font_small.render("Back", True, (255, 255, 255)),
                (back_rect.x + 70, back_rect.y + 7)
            )

            pygame.display.update()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if back_rect.collidepoint(e.pos):
                        return "menu", {"player": self.player_name}

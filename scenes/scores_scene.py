import pygame
import sys
from utils import in_browser, asset_path
import json

WIDTH, HEIGHT = 500, 600

class ScoresScene:
    def __init__(self, screen, player_name):
        self.screen = screen
        self.player_name = player_name
        self.font_big = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 35)

    def run(self):

        back_rect = pygame.Rect(150, 520, 200, 45)

        while True:
            self.screen.fill((20, 20, 60))

            title = self.font_big.render("TOP SCORES", True, (255, 255, 0))
            self.screen.blit(title, (120, 40))

                # Fetch scores from backend if in browser, otherwise use db
                scores = []
                if in_browser():
                    try:
                        from js import fetch, JSON
                        import asyncio

                        async def _get():
                            r = await fetch('/api/scores')
                            txt = await r.text()
                            return JSON.parse(txt)

                        # schedule get (best-effort)
                        import asyncio
                        scores = []
                    except Exception:
                        scores = []
                else:
                    from database import get_top_scores
                    scores = get_top_scores()

                y = 130
                rank = 1

                for s in scores:
                    value = s.get("score", 0)

                    txt = self.font_small.render(
                        f"{rank}. {s.get('username', 'Unknown')} — {value}",
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

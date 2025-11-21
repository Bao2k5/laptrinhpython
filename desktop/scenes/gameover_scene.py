import pygame
import sys
import asyncio
from utils import asset_path, in_browser

WIDTH, HEIGHT = 500, 600

class GameOverScene:
    def __init__(self, screen, player_name, score):
        self.screen = screen
        self.player_name = player_name
        self.score = score

        self.bg = pygame.image.load(asset_path('assets', 'gameover_bg.png')).convert()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

        self.font_big = pygame.font.Font(None, 70)
        self.font_small = pygame.font.Font(None, 40)

    async def run(self):
        restart_rect = pygame.Rect(150, 330, 200, 50)
        menu_rect = pygame.Rect(150, 400, 200, 50)
        quit_rect = pygame.Rect(150, 470, 200, 50)

        while True:
            await asyncio.sleep(0)
            self.screen.blit(self.bg, (0, 0))

            # Title
            title = self.font_big.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(title, (100, 140))

            # Player
            txt = self.font_small.render(f"Player: {self.player_name}", True, (255, 255, 255))
            self.screen.blit(txt, (130, 220))

            # Score
            txt = self.font_small.render(f"Score: {self.score}", True, (255, 255, 0))
            self.screen.blit(txt, (180, 270))

            # Buttons
            self.draw_button(restart_rect, "Restart", (0, 200, 0))
            self.draw_button(menu_rect, "Menu", (30, 120, 255))
            self.draw_button(quit_rect, "Quit", (200, 30, 30))

            pygame.display.update()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        return "menu", {"player": self.player_name}

                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if restart_rect.collidepoint(e.pos):
                        return "play", {"player": self.player_name}

                    if menu_rect.collidepoint(e.pos):
                        return "menu", {"player": self.player_name}

                    if quit_rect.collidepoint(e.pos):
                        pygame.quit()
                        sys.exit()

    def draw_button(self, rect, text, color):
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        txt = self.font_small.render(text, True, (255, 255, 255))
        self.screen.blit(txt, (rect.centerx - txt.get_width() // 2,
                               rect.centery - txt.get_height() // 2))

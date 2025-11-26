
import pygame
import sys
from utils import asset_path


class MenuScene:
    def __init__(self, screen, player_name):
        self.screen = screen
        self.player_name = player_name or "Unknown"
        self.font_title = pygame.font.Font(None, 70)
        self.font_small = pygame.font.Font(None, 32)

        self.bg = pygame.image.load(asset_path('assets', 'menu_bg.png')).convert()
        self.bg = pygame.transform.scale(self.bg, (500, 600))

        self.btn_play = pygame.image.load(asset_path('assets', 'play_btn.png')).convert_alpha()
        self.btn_play_hover = pygame.image.load(asset_path('assets', 'play_btn_hover.png')).convert_alpha()

        self.btn_scores = pygame.image.load(asset_path('assets', 'play_btn.png')).convert_alpha()
        self.btn_scores_hover = pygame.image.load(asset_path('assets', 'play_btn_hover.png')).convert_alpha()

        self.btn_quit = pygame.image.load(asset_path('assets', 'quit_btn.png')).convert_alpha()
        self.btn_quit_hover = pygame.image.load(asset_path('assets', 'quit_btn_hover.png')).convert_alpha()

        self.btn_w, self.btn_h = 200, 50

        self.btn_play = pygame.transform.scale(self.btn_play, (self.btn_w, self.btn_h))
        self.btn_play_hover = pygame.transform.scale(self.btn_play_hover, (self.btn_w, self.btn_h))

        self.btn_scores = pygame.transform.scale(self.btn_scores, (self.btn_w, self.btn_h))
        self.btn_scores_hover = pygame.transform.scale(self.btn_scores_hover, (self.btn_w, self.btn_h))

        self.btn_quit = pygame.transform.scale(self.btn_quit, (self.btn_w, self.btn_h))
        self.btn_quit_hover = pygame.transform.scale(self.btn_quit_hover, (self.btn_w, self.btn_h))

    def run(self):
        play_rect = pygame.Rect(150, 260, self.btn_w, self.btn_h)
        scores_rect = pygame.Rect(150, 330, self.btn_w, self.btn_h)
        quit_rect = pygame.Rect(150, 400, self.btn_w, self.btn_h)

        while True:
            self.screen.blit(self.bg, (0, 0))
            mx, my = pygame.mouse.get_pos()

            title = self.font_title.render("FLAPPY BIRD", True, (255, 255, 0))
            self.screen.blit(title, (70, 120))

            player_text = self.font_small.render(f"Player: {self.player_name}", True, (255, 255, 255))
            self.screen.blit(player_text, (10, 10))

            # Play
            self.screen.blit(
                self.btn_play_hover if play_rect.collidepoint((mx, my)) else self.btn_play,
                play_rect
            )
            txt = self.font_small.render("Play", True, (255, 255, 255))
            self.screen.blit(txt, (play_rect.centerx - txt.get_width() // 2,
                                   play_rect.centery - txt.get_height() // 2))

            # Scores
            self.screen.blit(
                self.btn_scores_hover if scores_rect.collidepoint((mx, my)) else self.btn_scores,
                scores_rect
            )
            txt = self.font_small.render("Scores", True, (255, 255, 255))
            self.screen.blit(txt, (scores_rect.centerx - txt.get_width() // 2,
                                   scores_rect.centery - txt.get_height() // 2))

            # Quit
            self.screen.blit(
                self.btn_quit_hover if quit_rect.collidepoint((mx, my)) else self.btn_quit,
                quit_rect
            )
            txt = self.font_small.render("Quit", True, (255, 255, 255))
            self.screen.blit(txt, (quit_rect.centerx - txt.get_width() // 2,
                                   quit_rect.centery - txt.get_height() // 2))

            pygame.display.update()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if play_rect.collidepoint(e.pos):
                        return "play", {"player": self.player_name}

                    if scores_rect.collidepoint(e.pos):
                        return "scores", {"player": self.player_name}  # FIX ✔

                    if quit_rect.collidepoint(e.pos):
                        pygame.quit()
                        sys.exit()

import pygame
import sys
import asyncio
from game_utils import asset_path, load_sound

class MenuScene:
    def __init__(self, screen, player_name):
        self.screen = screen
        self.player_name = player_name or "Unknown"
        self.font_title = pygame.font.Font(None, 70)
        self.font_small = pygame.font.Font(None, 32)
        self.font = self.font_small # Alias for convenience

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
        
        self.click_sound = load_sound('assets/flap.wav')

    async def run(self):
        WIDTH = self.screen.get_width()
        
        # Adjusted Y positions to fit 5 buttons in 600px height
        # Start higher (250) and use smaller gap (60)
        play_rect = pygame.Rect(WIDTH//2 - 100, 250, 200, 50)
        shop_rect = pygame.Rect(WIDTH//2 - 100, 310, 200, 50)
        scores_rect = pygame.Rect(WIDTH//2 - 100, 370, 200, 50)
        train_rect = pygame.Rect(WIDTH//2 - 100, 430, 200, 50)
        quit_rect = pygame.Rect(WIDTH//2 - 100, 490, 200, 50)

        while True:
            await asyncio.sleep(0)
            self.screen.blit(self.bg, (0, 0))
            mx, my = pygame.mouse.get_pos()

            title = self.font_title.render("FLAPPY BIRD", True, (255, 255, 0))
            title_shadow = self.font_title.render("FLAPPY BIRD", True, (0, 0, 0))
            self.screen.blit(title_shadow, (73, 103)) # Moved title up slightly
            self.screen.blit(title, (70, 100))

            player_text = self.font_small.render(f"Player: {self.player_name}", True, (255, 255, 255))
            self.screen.blit(player_text, (10, 10))

            # --- DRAW BUTTONS ---
            
            # Play Button
            pygame.draw.rect(self.screen, (0, 200, 0), play_rect, border_radius=10)
            if play_rect.collidepoint(mx, my):
                pygame.draw.rect(self.screen, (0, 255, 0), play_rect, border_radius=10, width=3)
            play_text = self.font.render("PLAY", True, (255, 255, 255))
            self.screen.blit(play_text, (WIDTH//2 - play_text.get_width()//2, 265))

            # Shop Button
            pygame.draw.rect(self.screen, (255, 165, 0), shop_rect, border_radius=10)
            if shop_rect.collidepoint(mx, my):
                pygame.draw.rect(self.screen, (255, 200, 0), shop_rect, border_radius=10, width=3)
            shop_text = self.font.render("SHOP", True, (255, 255, 255))
            self.screen.blit(shop_text, (WIDTH//2 - shop_text.get_width()//2, 325))

            # Scores Button
            pygame.draw.rect(self.screen, (0, 0, 200), scores_rect, border_radius=10)
            if scores_rect.collidepoint(mx, my):
                pygame.draw.rect(self.screen, (50, 50, 255), scores_rect, border_radius=10, width=3)
            scores_text = self.font.render("RANK", True, (255, 255, 255))
            self.screen.blit(scores_text, (WIDTH//2 - scores_text.get_width()//2, 385))

            # Train AI Button
            pygame.draw.rect(self.screen, (128, 0, 128), train_rect, border_radius=10)
            if train_rect.collidepoint(mx, my):
                pygame.draw.rect(self.screen, (180, 0, 180), train_rect, border_radius=10, width=3)
            train_text = self.font.render("TRAIN AI", True, (255, 255, 255))
            self.screen.blit(train_text, (WIDTH//2 - train_text.get_width()//2, 445))

            # Quit Button
            pygame.draw.rect(self.screen, (200, 0, 0), quit_rect, border_radius=10)
            if quit_rect.collidepoint(mx, my):
                pygame.draw.rect(self.screen, (255, 50, 50), quit_rect, border_radius=10, width=3)
            quit_text = self.font.render("QUIT", True, (255, 255, 255))
            self.screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, 505))

            pygame.display.update()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if play_rect.collidepoint(e.pos):
                        if self.click_sound: self.click_sound.play()
                        return "play", {"player": self.player_name}

                    if shop_rect.collidepoint(e.pos):
                        if self.click_sound: self.click_sound.play()
                        return "shop", {"player": self.player_name}

                    if scores_rect.collidepoint(e.pos):
                        if self.click_sound: self.click_sound.play()
                        return "scores", {"player": self.player_name}

                    if train_rect.collidepoint(e.pos):
                        if self.click_sound: self.click_sound.play()
                        return "train", {"player": self.player_name}

                    if quit_rect.collidepoint(e.pos):
                        pygame.quit()
                        sys.exit()

import pygame
import sys
import asyncio
from local_storage import LocalStorage

WIDTH, HEIGHT = 500, 600

class LoginScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 28)
        self.font_tiny = pygame.font.Font(None, 20)
        
        # Load saved data
        self.storage = LocalStorage()
        self.saved_username = self.storage.get_username()

    async def run(self):
        # Auto-login if username exists
        if self.saved_username and self.saved_username != "Guest":
            return "menu", {"player": self.saved_username}
        
        # First time - ask for nickname
        nickname = ""
        cursor_timer = 0
        error_msg = ""

        while True:
            await asyncio.sleep(0)
            self.screen.fill((30, 30, 40))  # Dark background

            # Cursor logic
            cursor_timer += 1
            show_cursor = (cursor_timer // 30) % 2 == 0

            # Title
            title = self.font.render("WELCOME TO FLAPPY BIRD", True, (255, 215, 0))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))

            # Subtitle
            subtitle = self.font_small.render("Enter your nickname to start", True, (200, 200, 200))
            self.screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 140))

            # Nickname input
            lbl_nickname = self.font.render("Nickname:", True, (200, 200, 200))
            self.screen.blit(lbl_nickname, (120, 220))
            
            input_color = (100, 100, 120)
            input_border = (255, 255, 255)
            
            pygame.draw.rect(self.screen, input_color, (120, 250, 260, 40))
            pygame.draw.rect(self.screen, input_border, (120, 250, 260, 40), 2)
            
            # Display nickname with cursor
            nickname_txt = nickname + ("_" if show_cursor else "")
            txt_surf = self.font.render(nickname_txt, True, (255, 255, 255))
            self.screen.blit(txt_surf, (130, 258))

            # Info text
            info_lines = [
                "Your ID will be automatically generated",
                "based on your device",
                "",
                "You can find your ID in the menu"
            ]
            for i, line in enumerate(info_lines):
                info_surf = self.font_tiny.render(line, True, (150, 150, 150))
                self.screen.blit(info_surf, (WIDTH//2 - info_surf.get_width()//2, 320 + i * 25))

            # Start button
            start_rect = pygame.Rect(WIDTH//2 - 60, 450, 120, 50)
            
            # Hover effect
            mouse_pos = pygame.mouse.get_pos()
            start_color = (60, 220, 140) if start_rect.collidepoint(mouse_pos) else (50, 200, 120)

            pygame.draw.rect(self.screen, start_color, start_rect, border_radius=5)
            
            start_txt = self.font.render("START", True, (255, 255, 255))
            self.screen.blit(start_txt, (start_rect.centerx - start_txt.get_width()//2, 
                                        start_rect.centery - start_txt.get_height()//2))

            # Error message
            if error_msg:
                err_surf = self.font_small.render(error_msg, True, (255, 100, 100))
                self.screen.blit(err_surf, (WIDTH//2 - err_surf.get_width()//2, 520))

            pygame.display.update()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.MOUSEBUTTONDOWN:
                    # Start button
                    if start_rect.collidepoint(e.pos):
                        if nickname.strip():
                            # Save nickname
                            self.storage.set_username(nickname.strip())
                            return "menu", {"player": nickname.strip()}
                        else:
                            error_msg = "Please enter a nickname!"

                if e.type == pygame.KEYDOWN:
                    error_msg = ""  # Clear error on typing
                    
                    if e.key == pygame.K_BACKSPACE:
                        nickname = nickname[:-1]

                    elif e.key == pygame.K_RETURN:
                        if nickname.strip():
                            self.storage.set_username(nickname.strip())
                            return "menu", {"player": nickname.strip()}
                        else:
                            error_msg = "Please enter a nickname!"

                    else:
                        # Limit length to 12 characters
                        if len(nickname) < 12 and e.unicode.isprintable():
                            nickname += e.unicode

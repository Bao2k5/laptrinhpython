import pygame
import sys
import asyncio
from utils import in_browser, asset_path

class RegisterScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)

    async def run(self):
        username = ""
        password = ""
        active = "user"
        cursor_timer = 0
        error_msg = ""
        WIDTH = 500 # Assuming width

        while True:
            await asyncio.sleep(0)
            self.screen.fill((30, 30, 40))

            title = self.font.render("REGISTER", True, (255, 215, 0))
            self.screen.blit(title, (180, 60))

            # Cursor logic
            cursor_timer += 1
            show_cursor = (cursor_timer // 30) % 2 == 0

            # --- USERNAME ---
            lbl_user = self.font.render("Username:", True, (200, 200, 200))
            self.screen.blit(lbl_user, (120, 140))

            user_color = (100, 100, 120) if active == "user" else (70, 70, 80)
            user_border = (255, 255, 255) if active == "user" else (100, 100, 100)

            pygame.draw.rect(self.screen, user_color, (120, 170, 260, 40))
            pygame.draw.rect(self.screen, user_border, (120, 170, 260, 40), 2)

            user_txt = username + ("|" if active == "user" and show_cursor else "")
            txt_surf = self.font.render(user_txt, True, (255, 255, 255))
            self.screen.blit(txt_surf, (130, 178))

            # --- PASSWORD ---
            lbl_pass = self.font.render("Password:", True, (200, 200, 200))
            self.screen.blit(lbl_pass, (120, 230))

            pass_color = (100, 100, 120) if active == "pass" else (70, 70, 80)
            pass_border = (255, 255, 255) if active == "pass" else (100, 100, 100)

            pygame.draw.rect(self.screen, pass_color, (120, 260, 260, 40))
            pygame.draw.rect(self.screen, pass_border, (120, 260, 260, 40), 2)

            pass_hidden = "*" * len(password) + ("|" if active == "pass" and show_cursor else "")
            txt_surf = self.font.render(pass_hidden, True, (255, 255, 255))
            self.screen.blit(txt_surf, (130, 268))

            # --- BUTTONS ---
            reg_rect = pygame.Rect(120, 340, 120, 50)
            back_rect = pygame.Rect(260, 340, 120, 50)

            mouse_pos = pygame.mouse.get_pos()
            reg_color = (60, 220, 140) if reg_rect.collidepoint(mouse_pos) else (50, 200, 120)
            back_color = (200, 100, 100) if back_rect.collidepoint(mouse_pos) else (180, 80, 80)

            pygame.draw.rect(self.screen, reg_color, reg_rect, border_radius=5)
            pygame.draw.rect(self.screen, back_color, back_rect, border_radius=5)

            reg_txt = self.font.render("Create", True, (255, 255, 255))
            back_txt = self.font.render("Back", True, (255, 255, 255))

            self.screen.blit(reg_txt, (reg_rect.centerx - reg_txt.get_width()//2, reg_rect.centery - reg_txt.get_height()//2))
            self.screen.blit(back_txt, (back_rect.centerx - back_txt.get_width()//2, back_rect.centery - back_txt.get_height()//2))

            # --- ERROR MESSAGE ---
            if error_msg:
                err_surf = self.font.render(error_msg, True, (255, 100, 100))
                self.screen.blit(err_surf, (WIDTH//2 - err_surf.get_width()//2, 420))

            pygame.display.update()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.MOUSEBUTTONDOWN:
                    # Click to focus
                    if pygame.Rect(120, 170, 260, 40).collidepoint(e.pos):
                        active = "user"
                    elif pygame.Rect(120, 260, 260, 40).collidepoint(e.pos):
                        active = "pass"

                    if reg_rect.collidepoint(e.pos):
                        if in_browser():
                            error_msg = "Web Register..."
                        else:
                            from database import create_user
                            if create_user(username, password):
                                return "login", {}
                            else:
                                error_msg = "User exists!"

                    if back_rect.collidepoint(e.pos):
                        return "login", {}

                if e.type == pygame.KEYDOWN:
                    error_msg = ""
                    if e.key == pygame.K_TAB:
                        active = "pass" if active == "user" else "user"

                    elif e.key == pygame.K_BACKSPACE:
                        if active == "user":
                            username = username[:-1]
                        else:
                            password = password[:-1]

                    else:
                        if active == "user" and len(username) < 12:
                            username += e.unicode
                        elif active == "pass" and len(password) < 12:
                            password += e.unicode

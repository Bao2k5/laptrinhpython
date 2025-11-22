import pygame
import sys
import asyncio
from database import check_login
from game_utils import in_browser

WIDTH, HEIGHT = 500, 600

class LoginScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.input_user = ""
        self.input_pass = ""
        self.is_password = True

    async def run(self):
        username = ""
        password = ""
        active = "user"
        cursor_timer = 0
        error_msg = ""

        while True:
            await asyncio.sleep(0)
            self.screen.fill((30, 30, 40))  # Slightly lighter background

            # Title
            title = self.font.render("LOGIN", True, (255, 215, 0))  # Gold color
            self.screen.blit(title, (200, 60))

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
            
            # Horizontal cursor (underscore)
            user_txt = username + ("_" if active == "user" and show_cursor else "")
            txt_surf = self.font.render(user_txt, True, (255, 255, 255))
            self.screen.blit(txt_surf, (130, 178))

            # --- PASSWORD ---
            lbl_pass = self.font.render("Password:", True, (200, 200, 200))
            self.screen.blit(lbl_pass, (120, 230))

            pass_color = (100, 100, 120) if active == "pass" else (70, 70, 80)
            pass_border = (255, 255, 255) if active == "pass" else (100, 100, 100)

            pygame.draw.rect(self.screen, pass_color, (120, 260, 260, 40))
            pygame.draw.rect(self.screen, pass_border, (120, 260, 260, 40), 2)

            # Horizontal cursor (underscore)
            pass_hidden = "*" * len(password) + ("_" if active == "pass" and show_cursor else "")
            txt_surf = self.font.render(pass_hidden, True, (255, 255, 255))
            self.screen.blit(txt_surf, (130, 268))

            # --- BUTTONS ---
            login_rect = pygame.Rect(120, 340, 120, 50)
            register_rect = pygame.Rect(260, 340, 120, 50)

            # Hover effects
            mouse_pos = pygame.mouse.get_pos()
            
            login_color = (60, 180, 240) if login_rect.collidepoint(mouse_pos) else (50, 150, 200)
            reg_color = (60, 220, 140) if register_rect.collidepoint(mouse_pos) else (50, 200, 120)

            pygame.draw.rect(self.screen, login_color, login_rect, border_radius=5)
            pygame.draw.rect(self.screen, reg_color, register_rect, border_radius=5)

            login_txt = self.font.render("Login", True, (255, 255, 255))
            reg_txt = self.font.render("Register", True, (255, 255, 255))

            self.screen.blit(login_txt, (login_rect.centerx - login_txt.get_width()//2, login_rect.centery - login_txt.get_height()//2))
            self.screen.blit(reg_txt, (register_rect.centerx - reg_txt.get_width()//2, register_rect.centery - reg_txt.get_height()//2))

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

                    if login_rect.collidepoint(e.pos):
                        if in_browser():
                            error_msg = "Login via Web API..."
                            # Implement web login here if needed, or just warn
                        else:
                            from database import check_login
                            if check_login(username, password):
                                return "menu", {"player": username}
                            else:
                                error_msg = "Login Failed!"

                    if register_rect.collidepoint(e.pos):
                        return "register", {}

                if e.type == pygame.KEYDOWN:
                    error_msg = ""  # Clear error on typing
                    if e.key == pygame.K_TAB:
                        active = "pass" if active == "user" else "user"

                    elif e.key == pygame.K_BACKSPACE:
                        if active == "user":
                            username = username[:-1]
                        else:
                            password = password[:-1]

                    elif e.key == pygame.K_RETURN:
                        if in_browser():
                             error_msg = "Web Login..."
                        else:
                            from database import check_login
                            if check_login(username, password):
                                return "menu", {"player": username}
                            else:
                                error_msg = "Login Failed!"

                    else:
                        # Limit length
                        if active == "user" and len(username) < 12:
                            username += e.unicode
                        elif active == "pass" and len(password) < 12:
                            password += e.unicode

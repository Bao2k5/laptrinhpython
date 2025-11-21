import pygame
import sys
import asyncio
from database import check_login
from utils import in_browser

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

        while True:
            await asyncio.sleep(0)
            self.screen.fill((20, 20, 30))

            title = self.font.render("LOGIN", True, (255, 255, 0))
            self.screen.blit(title, (200, 80))

            # Username input
            pygame.draw.rect(self.screen, (80, 80, 80), (120, 180, 260, 40))
            txt = self.font.render(username, True, (255, 255, 255))
            self.screen.blit(txt, (130, 185))

            # Password input
            pygame.draw.rect(self.screen, (80, 80, 80), (120, 240, 260, 40))
            hidden = "*" * len(password)
            txt = self.font.render(hidden, True, (255, 255, 255))
            self.screen.blit(txt, (130, 245))

            # Buttons
            login_rect = pygame.Rect(180, 320, 155, 45)
            register_rect = pygame.Rect(180, 380, 155, 45)

            pygame.draw.rect(self.screen, (50, 150, 200), login_rect)
            pygame.draw.rect(self.screen, (50, 200, 120), register_rect)

            self.screen.blit(self.font.render("LOGIN", True, (255, 255, 255)),
                             (login_rect.x + 30, login_rect.y + 10))
            self.screen.blit(self.font.render("REGISTER", True, (255, 255, 255)),
                             (register_rect.x + 10, register_rect.y + 10))

            pygame.display.update()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.MOUSEBUTTONDOWN:
                    if login_rect.collidepoint(e.pos):
                            if in_browser():
                                # Browser should use backend API for auth
                                print("Login not available in browser build. Use backend API.")
                            else:
                                from database import check_login
                                if check_login(username, password):
                                    return "menu", {"player": username}
                                else:
                                    print("LOGIN FAILED")

                    if register_rect.collidepoint(e.pos):
                        return "register", {}

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_TAB:
                        active = "pass" if active == "user" else "user"

                    elif e.key == pygame.K_BACKSPACE:
                        if active == "user":
                            username = username[:-1]
                        else:
                            password = password[:-1]

                    elif e.key == pygame.K_RETURN:
                            if in_browser():
                                print("Login not available in browser build. Use backend API.")
                            else:
                                from database import check_login
                                if check_login(username, password):
                                    return "menu", {"player": username}

                    else:
                        if active == "user" and len(username) < 12:
                            username += e.unicode
                        elif active == "pass" and len(password) < 12:
                            password += e.unicode

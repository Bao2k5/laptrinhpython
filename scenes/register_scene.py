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

        while True:
            await asyncio.sleep(0)
            self.screen.fill((20, 20, 40))

            title = self.font.render("REGISTER", True, (255, 255, 0))
            self.screen.blit(title, (180, 80))

            # Inputs
            pygame.draw.rect(self.screen, (80, 80, 80), (120, 180, 260, 40))
            pygame.draw.rect(self.screen, (80, 80, 80), (120, 240, 260, 40))

            txt_u = self.font.render(username, True, (255, 255, 255))
            txt_p = self.font.render("*" * len(password), True, (255, 255, 255))

            self.screen.blit(txt_u, (130, 185))
            self.screen.blit(txt_p, (130, 245))

            # buttons
            reg_rect = pygame.Rect(180, 320, 140, 45)
            back_rect = pygame.Rect(180, 380, 140, 45)

            pygame.draw.rect(self.screen, (50, 200, 120), reg_rect)
            pygame.draw.rect(self.screen, (180, 80, 80), back_rect)

            self.screen.blit(self.font.render("CREATE", True, (255, 255, 255)),
                             (reg_rect.x + 30, reg_rect.y + 10))
            self.screen.blit(self.font.render("BACK", True, (255, 255, 255)),
                             (back_rect.x + 40, back_rect.y + 10))

            pygame.display.update()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.MOUSEBUTTONDOWN:
                    if reg_rect.collidepoint(e.pos):
                        if in_browser():
                            # In browser, registration should go through backend API.
                            print("Registration is disabled in the browser build. Use backend API.")
                            return "login", {}
                        else:
                            from database import create_user
                            if create_user(username, password):
                                return "login", {}
                            else:
                                print("User exists!")

                    if back_rect.collidepoint(e.pos):
                        return "login", {}

                if e.type == pygame.KEYDOWN:
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

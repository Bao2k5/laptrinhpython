import pygame
import sys
import asyncio
from database import check_login
from game_utils import in_browser
from local_storage import LocalStorage

WIDTH, HEIGHT = 500, 600

class LoginScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 28)
        self.input_user = ""
        self.input_pass = ""
        self.is_password = True
        
        # Load saved username from LocalStorage
        self.storage = LocalStorage()
        self.saved_username = self.storage.get_username()

    async def run(self):
        # Pre-fill username if saved
        username = ""
        password = ""
        active = "user"
        cursor_timer = 0
        error_msg = ""
        remember_me = False
        
        # Get saved accounts
        saved_accounts = self.storage.get_saved_accounts()
        selected_account = None

        while True:
            await asyncio.sleep(0)
            self.screen.fill((30, 30, 40))  # Dark background

            # Cursor logic
            cursor_timer += 1
            show_cursor = (cursor_timer // 30) % 2 == 0

            # --- SAVED ACCOUNTS PANEL (LEFT SIDE) ---
            if saved_accounts:
                panel_x, panel_y = 10, 60
                panel_w, panel_h = 140, HEIGHT - 70
                
                pygame.draw.rect(self.screen, (40, 40, 50), (panel_x, panel_y, panel_w, panel_h), border_radius=8)
                pygame.draw.rect(self.screen, (80, 80, 100), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=8)
                
                # Title
                title_surf = self.font_small.render("Saved", True, (200, 200, 200))
                self.screen.blit(title_surf, (panel_x + panel_w//2 - title_surf.get_width()//2, panel_y + 10))
                
                # Account list
                mouse_pos = pygame.mouse.get_pos()
                for i, acc in enumerate(saved_accounts):
                    acc_y = panel_y + 50 + i * 50
                    acc_rect = pygame.Rect(panel_x + 5, acc_y, panel_w - 10, 45)
                    
                    # Hover effect
                    if acc_rect.collidepoint(mouse_pos):
                        pygame.draw.rect(self.screen, (60, 120, 200), acc_rect, border_radius=5)
                    else:
                        pygame.draw.rect(self.screen, (50, 50, 60), acc_rect, border_radius=5)
                    
                    # Username (truncate if too long)
                    acc_text = acc if len(acc) <= 10 else acc[:8] + ".."
                    acc_surf = self.font_small.render(acc_text, True, (255, 255, 255))
                    self.screen.blit(acc_surf, (panel_x + 10, acc_y + 5))
                    
                    # Delete button (X)
                    delete_rect = pygame.Rect(panel_x + panel_w - 25, acc_y + 5, 20, 20)
                    delete_color = (255, 100, 100) if delete_rect.collidepoint(mouse_pos) else (150, 50, 50)
                    pygame.draw.circle(self.screen, delete_color, delete_rect.center, 10)
                    x_surf = self.font_small.render("x", True, (255, 255, 255))
                    self.screen.blit(x_surf, (delete_rect.x + 4, delete_rect.y))

            # --- MAIN LOGIN FORM (RIGHT SIDE) ---
            form_x = 160 if saved_accounts else 120
            
            # Title
            title = self.font.render("LOGIN", True, (255, 215, 0))  # Gold color
            self.screen.blit(title, (form_x + 80, 60))

            # --- USERNAME ---
            lbl_user = self.font.render("Username:", True, (200, 200, 200))
            self.screen.blit(lbl_user, (form_x, 140))
            
            user_color = (100, 100, 120) if active == "user" else (70, 70, 80)
            user_border = (255, 255, 255) if active == "user" else (100, 100, 100)
            
            pygame.draw.rect(self.screen, user_color, (form_x, 170, 260, 40))
            pygame.draw.rect(self.screen, user_border, (form_x, 170, 260, 40), 2)
            
            # Horizontal cursor (underscore)
            user_txt = username + ("_" if active == "user" and show_cursor else "")
            txt_surf = self.font.render(user_txt, True, (255, 255, 255))
            self.screen.blit(txt_surf, (form_x + 10, 178))

            # --- PASSWORD ---
            lbl_pass = self.font.render("Password:", True, (200, 200, 200))
            self.screen.blit(lbl_pass, (form_x, 230))

            pass_color = (100, 100, 120) if active == "pass" else (70, 70, 80)
            pass_border = (255, 255, 255) if active == "pass" else (100, 100, 100)

            pygame.draw.rect(self.screen, pass_color, (form_x, 260, 260, 40))
            pygame.draw.rect(self.screen, pass_border, (form_x, 260, 260, 40), 2)

            # Horizontal cursor (underscore)
            pass_hidden = "*" * len(password) + ("_" if active == "pass" and show_cursor else "")
            txt_surf = self.font.render(pass_hidden, True, (255, 255, 255))
            self.screen.blit(txt_surf, (form_x + 10, 268))

            # --- REMEMBER ME CHECKBOX ---
            checkbox_rect = pygame.Rect(form_x, 320, 20, 20)
            checkbox_color = (100, 200, 100) if remember_me else (70, 70, 80)
            pygame.draw.rect(self.screen, checkbox_color, checkbox_rect, border_radius=3)
            pygame.draw.rect(self.screen, (150, 150, 150), checkbox_rect, 2, border_radius=3)
            
            if remember_me:
                # Draw checkmark
                pygame.draw.line(self.screen, (255, 255, 255), 
                               (checkbox_rect.x + 4, checkbox_rect.y + 10),
                               (checkbox_rect.x + 8, checkbox_rect.y + 16), 2)
                pygame.draw.line(self.screen, (255, 255, 255),
                               (checkbox_rect.x + 8, checkbox_rect.y + 16),
                               (checkbox_rect.x + 16, checkbox_rect.y + 4), 2)
            
            remember_txt = self.font_small.render("Remember Me", True, (200, 200, 200))
            self.screen.blit(remember_txt, (form_x + 30, 318))

            # --- BUTTONS ---
            login_rect = pygame.Rect(form_x, 360, 120, 50)
            register_rect = pygame.Rect(form_x + 140, 360, 120, 50)

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
                self.screen.blit(err_surf, (WIDTH//2 - err_surf.get_width()//2, 440))

            pygame.display.update()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.MOUSEBUTTONDOWN:
                    # Click to focus input fields
                    if pygame.Rect(form_x, 170, 260, 40).collidepoint(e.pos):
                        active = "user"
                    elif pygame.Rect(form_x, 260, 260, 40).collidepoint(e.pos):
                        active = "pass"
                    
                    # Remember me checkbox
                    elif checkbox_rect.collidepoint(e.pos):
                        remember_me = not remember_me
                    
                    # Saved accounts - click to auto-fill
                    elif saved_accounts:
                        for i, acc in enumerate(saved_accounts):
                            acc_y = 60 + 50 + i * 50
                            acc_rect = pygame.Rect(15, acc_y, 130, 45)
                            delete_rect = pygame.Rect(15 + 130 - 25, acc_y + 5, 20, 20)
                            
                            if delete_rect.collidepoint(e.pos):
                                # Delete account
                                self.storage.remove_credentials(acc)
                                saved_accounts = self.storage.get_saved_accounts()
                                break
                            elif acc_rect.collidepoint(e.pos):
                                # Load credentials
                                creds = self.storage.get_credentials(acc)
                                if creds:
                                    username = creds["username"]
                                    password = creds["password"]
                                    remember_me = True
                                break

                    # Login button
                    if login_rect.collidepoint(e.pos):
                        if in_browser():
                            error_msg = "Login via Web API..."
                        else:
                            from database import check_login
                            if check_login(username, password):
                                # Save credentials if remember me is checked
                                if remember_me:
                                    self.storage.save_credentials(username, password)
                                return "menu", {"player": username}
                            else:
                                error_msg = "Login Failed!"

                    # Register button
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
                                # Save credentials if remember me is checked
                                if remember_me:
                                    self.storage.save_credentials(username, password)
                                return "menu", {"player": username}
                            else:
                                error_msg = "Login Failed!"

                    else:
                        # Limit length
                        if active == "user" and len(username) < 12:
                            username += e.unicode
                        elif active == "pass" and len(password) < 12:
                            password += e.unicode

"""
Pause Menu va Settings Menu cho Flappy Bird
"""
import pygame
import os
from settings import get_settings

# Constants
WIN_WIDTH = 500
WIN_HEIGHT = 800

class UIButton:
    """Button class don gian cho UI"""
    def __init__(self, x, y, image_path, scale=1.0):
        try:
            self.image = pygame.image.load(image_path)
            width = int(self.image.get_width() * scale)
            height = int(self.image.get_height() * scale)
            self.image = pygame.transform.scale(self.image, (width, height))
        except:
            # Fallback: tao button don gian
            self.image = pygame.Surface((200, 60))
            self.image.fill((100, 100, 100))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False
        self.hover = False

    def draw(self, screen):
        """Ve button va kiem tra click"""
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.hover = True
            # Phong to khi hover
            enlarged = pygame.transform.scale(
                self.image,
                (int(self.image.get_width() * 1.1), int(self.image.get_height() * 1.1))
            )
            enlarged_rect = enlarged.get_rect(center=self.rect.center)
            screen.blit(enlarged, enlarged_rect)

            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        else:
            self.hover = False
            screen.blit(self.image, self.rect)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action

class Slider:
    """Slider cho volume control"""
    def __init__(self, x, y, width, height, min_val=0.0, max_val=1.0, initial_val=0.5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val

        self.dragging = False

        # Colors
        self.track_color = (80, 80, 80)
        self.fill_color = (0, 150, 255)
        self.handle_color = (200, 200, 200)
        self.handle_hover_color = (255, 255, 255)

        self.handle_radius = 12

    def get_handle_x(self):
        """Tinh vi tri x cua handle"""
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        return self.x + int(ratio * self.width)

    def draw(self, screen):
        """Ve slider"""
        # Ve track
        track_rect = pygame.Rect(self.x, self.y - self.height//2, self.width, self.height)
        pygame.draw.rect(screen, self.track_color, track_rect, border_radius=self.height//2)

        # Ve fill (phan da dien)
        handle_x = self.get_handle_x()
        fill_width = handle_x - self.x
        if fill_width > 0:
            fill_rect = pygame.Rect(self.x, self.y - self.height//2, fill_width, self.height)
            pygame.draw.rect(screen, self.fill_color, fill_rect, border_radius=self.height//2)

        # Ve handle
        pos = pygame.mouse.get_pos()
        handle_center = (handle_x, self.y)
        distance = ((pos[0] - handle_center[0])**2 + (pos[1] - handle_center[1])**2)**0.5

        if distance < self.handle_radius * 2 or self.dragging:
            color = self.handle_hover_color
        else:
            color = self.handle_color

        pygame.draw.circle(screen, color, handle_center, self.handle_radius)
        pygame.draw.circle(screen, (255, 255, 255), handle_center, self.handle_radius, 2)

    def handle_event(self, event):
        """Xu ly event"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            handle_x = self.get_handle_x()
            distance = ((pos[0] - handle_x)**2 + (pos[1] - self.y)**2)**0.5

            if distance < self.handle_radius * 2:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            pos = pygame.mouse.get_pos()
            # Tinh gia tri moi
            ratio = (pos[0] - self.x) / self.width
            ratio = max(0, min(1, ratio))  # Clamp 0-1
            self.value = self.min_val + ratio * (self.max_val - self.min_val)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = max(self.min_val, min(self.max_val, value))

def show_pause_menu(screen):
    """
    Hien thi pause menu
    Returns: 'resume', 'restart', 'menu', None
    """
    clock = pygame.time.Clock()

    # Tao overlay trong suot
    overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))

    # Load buttons
    try:
        btn_resume = UIButton(WIN_WIDTH // 2, 300, "future_assets/ui/btn_resume_medium.png")
        btn_restart = UIButton(WIN_WIDTH // 2, 400, "future_assets/ui/btn_restart_medium.png")
        btn_settings = UIButton(WIN_WIDTH // 2, 500, "future_assets/ui/btn_settings_large.png", 0.8)
        btn_menu = UIButton(WIN_WIDTH // 2, 600, "future_assets/ui/btn_menu_medium.png")
    except:
        print("Khong load duoc buttons, dung text")
        btn_resume = None

    font_title = pygame.font.SysFont("comicsans", 80)
    font_hint = pygame.font.SysFont("comicsans", 30)

    running = True
    while running:
        clock.tick(30)

        # Ve overlay
        screen.blit(overlay, (0, 0))

        # Title
        title = font_title.render("PAUSED", True, (255, 215, 0))
        screen.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 150))

        # Buttons
        if btn_resume:
            if btn_resume.draw(screen):
                return 'resume'
            if btn_restart.draw(screen):
                return 'restart'
            if btn_settings.draw(screen):
                result = show_settings_menu(screen)
                if result == 'back':
                    pass  # Quay lai pause menu
            if btn_menu.draw(screen):
                return 'menu'
        else:
            # Fallback text menu
            hint = font_hint.render("Press ESC to resume", True, (255, 255, 255))
            screen.blit(hint, (WIN_WIDTH // 2 - hint.get_width() // 2, 400))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'menu'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'resume'
                if event.key == pygame.K_r:
                    return 'restart'
                if event.key == pygame.K_m:
                    return 'menu'

    return None

def show_settings_menu(screen):
    """
    Hien thi settings menu
    Returns: 'back'
    """
    settings = get_settings()
    clock = pygame.time.Clock()

    # Tao overlay
    overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((20, 20, 40))

    # Tao sliders
    master_slider = Slider(200, 250, 250, 10, 0.0, 1.0, settings.get_master_volume())
    music_slider = Slider(200, 350, 250, 10, 0.0, 1.0, settings.get_music_volume())
    sfx_slider = Slider(200, 450, 250, 10, 0.0, 1.0, settings.get_sfx_volume())

    # Button back
    try:
        btn_back = UIButton(WIN_WIDTH // 2, 650, "future_assets/ui/btn_back_small.png")
    except:
        btn_back = None

    font_title = pygame.font.SysFont("comicsans", 60)
    font_label = pygame.font.SysFont("comicsans", 35)
    font_value = pygame.font.SysFont("comicsans", 30)

    running = True
    while running:
        clock.tick(30)

        # Ve overlay
        screen.blit(overlay, (0, 0))

        # Title
        title = font_title.render("SETTINGS", True, (255, 215, 0))
        screen.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 80))

        # Master Volume
        label = font_label.render("Master Volume", True, (255, 255, 255))
        screen.blit(label, (50, 220))
        value_text = font_value.render(f"{int(master_slider.get_value() * 100)}%", True, (200, 200, 200))
        screen.blit(value_text, (460, 225))
        master_slider.draw(screen)

        # Music Volume
        label = font_label.render("Music Volume", True, (255, 255, 255))
        screen.blit(label, (50, 320))
        value_text = font_value.render(f"{int(music_slider.get_value() * 100)}%", True, (200, 200, 200))
        screen.blit(value_text, (460, 325))
        music_slider.draw(screen)

        # SFX Volume
        label = font_label.render("SFX Volume", True, (255, 255, 255))
        screen.blit(label, (50, 420))
        value_text = font_value.render(f"{int(sfx_slider.get_value() * 100)}%", True, (200, 200, 200))
        screen.blit(value_text, (460, 425))
        sfx_slider.draw(screen)

        # Hint
        hint_font = pygame.font.SysFont("comicsans", 25)
        hint = hint_font.render("Press ESC to go back", True, (150, 150, 150))
        screen.blit(hint, (WIN_WIDTH // 2 - hint.get_width() // 2, 550))

        # Back button
        if btn_back and btn_back.draw(screen):
            # Save settings
            settings.set_master_volume(master_slider.get_value())
            settings.set_music_volume(music_slider.get_value())
            settings.set_sfx_volume(sfx_slider.get_value())
            return 'back'

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Save before quit
                settings.set_master_volume(master_slider.get_value())
                settings.set_music_volume(music_slider.get_value())
                settings.set_sfx_volume(sfx_slider.get_value())
                return 'back'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Save settings
                    settings.set_master_volume(master_slider.get_value())
                    settings.set_music_volume(music_slider.get_value())
                    settings.set_sfx_volume(sfx_slider.get_value())
                    return 'back'

            # Handle slider events
            master_slider.handle_event(event)
            music_slider.handle_event(event)
            sfx_slider.handle_event(event)

    return 'back'

# Test
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("UI Test")

    # Test pause menu
    print("Testing Pause Menu...")
    result = show_pause_menu(screen)
    print(f"Result: {result}")

    pygame.quit()


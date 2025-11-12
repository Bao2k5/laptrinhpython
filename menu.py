import pygame
import sys

pygame.init()

# Constants
WIN_WIDTH = 500
WIN_HEIGHT = 800

class Button:
    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False
        self.hover = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.hover = True
            if not self.clicked:
                enlarged = pygame.transform.scale(self.image,
                    (int(self.image.get_width() * 1.05), int(self.image.get_height() * 1.05)))
                enlarged_rect = enlarged.get_rect(center=self.rect.center)
                surface.blit(enlarged, enlarged_rect)
            else:
                surface.blit(self.image, self.rect)

            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        else:
            self.hover = False
            surface.blit(self.image, self.rect)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action

def show_menu(screen):
    """Menu chinh - Return: 'play', 'start', 'help', 'exit'"""
    clock = pygame.time.Clock()

    try:
        menu_bg = pygame.image.load("imgs/menu_bg.png")
        menu_bg = pygame.transform.scale(menu_bg, (WIN_WIDTH, WIN_HEIGHT))
    except:
        menu_bg = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        menu_bg.fill((70, 130, 180))

    try:
        title_img = pygame.image.load("imgs/title.png")
        title_img = pygame.transform.scale(title_img, (450, 120))
    except:
        title_img = None

    try:
        btn_play_img = pygame.image.load("imgs/btn_play.png")
        btn_start_img = pygame.image.load("imgs/btn_start.png")
        btn_help_img = pygame.image.load("imgs/btn_help.png")
        btn_exit_img = pygame.image.load("imgs/btn_exit.png")

        btn_play = Button(WIN_WIDTH // 2, 320, btn_play_img, 0.8)
        btn_start = Button(WIN_WIDTH // 2, 430, btn_start_img, 0.8)
        btn_help = Button(WIN_WIDTH // 2, 540, btn_help_img, 0.8)
        btn_exit = Button(WIN_WIDTH // 2, 650, btn_exit_img, 0.8)
    except Exception as e:
        print(f"Error loading buttons: {e}")
        btn_play = None
        btn_start = None
        btn_help = None
        btn_exit = None

    running = True
    while running:
        clock.tick(60)
        screen.blit(menu_bg, (0, 0))

        if title_img:
            screen.blit(title_img, (25, 100))
        else:
            font = pygame.font.SysFont("comicsans", 80)
            title_text = font.render("FLAPPY BIRD", True, (255, 215, 0))
            title_shadow = font.render("FLAPPY BIRD", True, (0, 0, 0))
            screen.blit(title_shadow, (WIN_WIDTH // 2 - title_text.get_width() // 2 + 5, 105))
            screen.blit(title_text, (WIN_WIDTH // 2 - title_text.get_width() // 2, 100))

        font_small = pygame.font.SysFont("comicsans", 28)
        subtitle = font_small.render("Choose your mode:", True, (255, 255, 255))
        screen.blit(subtitle, (WIN_WIDTH // 2 - subtitle.get_width() // 2, 240))

        if btn_play and btn_start and btn_help and btn_exit:
            if btn_play.draw(screen):
                return 'play'
            if btn_start.draw(screen):
                return 'start'
            if btn_help.draw(screen):
                return 'help'
            if btn_exit.draw(screen):
                return 'exit'

            label_font = pygame.font.SysFont("comicsans", 20)
            play_label = label_font.render("(SPACE or BREATH control)", True, (200, 200, 200))
            start_label = label_font.render("(Watch AI play)", True, (200, 200, 200))
            screen.blit(play_label, (WIN_WIDTH // 2 - play_label.get_width() // 2, 365))
            screen.blit(start_label, (WIN_WIDTH // 2 - start_label.get_width() // 2, 475))
        else:
            font = pygame.font.SysFont("comicsans", 50)
            play_text = font.render("PLAY", True, (255, 255, 255))
            start_text = font.render("START AI", True, (255, 255, 255))
            help_text = font.render("HOW TO PLAY", True, (255, 255, 255))
            exit_text = font.render("EXIT", True, (255, 255, 255))

            screen.blit(play_text, (WIN_WIDTH // 2 - play_text.get_width() // 2, 320))
            screen.blit(start_text, (WIN_WIDTH // 2 - start_text.get_width() // 2, 430))
            screen.blit(help_text, (WIN_WIDTH // 2 - help_text.get_width() // 2, 540))
            screen.blit(exit_text, (WIN_WIDTH // 2 - exit_text.get_width() // 2, 650))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return 'play'
                if event.key == pygame.K_ESCAPE:
                    return 'exit'

        pygame.display.update()

    return 'exit'

def show_instructions(screen):
    """Hien thi man hinh huong dan"""
    clock = pygame.time.Clock()
    font_title = pygame.font.SysFont("comicsans", 60)
    font_text = pygame.font.SysFont("comicsans", 32)

    running = True
    while running:
        clock.tick(60)
        screen.fill((70, 130, 180))

        title = font_title.render("HOW TO PLAY", True, (255, 215, 0))
        screen.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 60))

        instructions = [
            "PLAYER MODE:",
            "• Press SPACE to jump",
            "• OR Blow into microphone",
            "• Avoid pipes and ground",
            "• Score saved to database",
            "",
            "AI MODE:",
            "• Watch AI learn to play",
            "• Uses NEAT algorithm",
            "• 50 generations",
            "",
            "4 LEVELS:",
            "• Level 1: 0-49 (EASY)",
            "• Level 2: 50-124 (MEDIUM)",
            "• Level 3: 125-249 (HARD)",
            "• Level 4: 250+ (EXTREME)",
            "",
            "Press SPACE to continue"
        ]

        y = 150
        for line in instructions:
            text = font_text.render(line, True, (255, 255, 255))
            screen.blit(text, (40, y))
            y += 38

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    return True

        pygame.display.update()

    return True

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird - Menu")
    choice = show_menu(screen)
    print(f"User choice: {choice}")
    if choice == 'help':
        show_instructions(screen)
    pygame.quit()


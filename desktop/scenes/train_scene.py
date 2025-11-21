import pygame
import sys
from flappy import train_ai  # dùng lại train_ai bạn đã viết
from utils import in_browser


class TrainScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)

    def run(self):
        # Màn hình thông báo
        self.screen.fill((10, 10, 20))
        txt = self.font.render("Đang train AI...", True, (255, 255, 0))
        self.screen.blit(txt, (120, 260))
        pygame.display.update()

        # Gọi train (sẽ tự mở loop, vẽ, ... như bạn code)
        if in_browser():
            # Training is heavy and should run server-side; show message and go back
            txt = self.font.render("Training disabled in browser. Use server.", True, (255, 255, 0))
            self.screen.blit(txt, (60,260))
            pygame.display.update()
            pygame.time.wait(1500)
            return "menu", {"player": None}
        else:
            train_ai()
            return "menu", {"player": None}

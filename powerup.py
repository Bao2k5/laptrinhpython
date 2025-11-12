"""
Power-up System cho Flappy Bird
Cac loai power-ups: Shield, Slow Motion, Magnet, Double Points
"""

import pygame
import os
import random

class PowerUp:
    """Class cho cac power-up items trong game"""

    # Power-up types
    SHIELD = "shield"
    SLOWMO = "slowmo"
    MAGNET = "magnet"
    DOUBLE_POINTS = "double_points"

    # Load images
    IMGS = {}

    @classmethod
    def load_images(cls):
        """Load tat ca power-up images"""
        try:
            cls.IMGS[cls.SHIELD] = pygame.image.load(
                os.path.join("future_assets", "powerups", "shield.png"))
            cls.IMGS[cls.SLOWMO] = pygame.image.load(
                os.path.join("future_assets", "powerups", "slowmo.png"))
            cls.IMGS[cls.MAGNET] = pygame.image.load(
                os.path.join("future_assets", "powerups", "magnet.png"))
            cls.IMGS[cls.DOUBLE_POINTS] = pygame.image.load(
                os.path.join("future_assets", "powerups", "double_points.png"))
            print("Power-up images loaded successfully!")
        except Exception as e:
            print(f"Error loading power-up images: {e}")

    def __init__(self, x, y, powerup_type=None):
        """
        Khoi tao power-up

        Args:
            x: Vi tri x
            y: Vi tri y
            powerup_type: Loai power-up (random neu None)
        """
        if not PowerUp.IMGS:
            PowerUp.load_images()

        # Random type neu khong chi dinh
        if powerup_type is None:
            powerup_type = random.choice([
                self.SHIELD, self.SLOWMO, self.MAGNET, self.DOUBLE_POINTS
            ])

        self.type = powerup_type
        self.img = PowerUp.IMGS.get(powerup_type)

        # Vi tri
        self.x = x
        self.y = y

        # Kich thuoc
        self.width = self.img.get_width() if self.img else 30
        self.height = self.img.get_height() if self.img else 30

        # Toc do di chuyen (cung toc voi pipes)
        self.vel = 5

        # Hieu ung
        self.float_offset = 0
        self.float_direction = 1
        self.rotation = 0

        # Thoi gian ton tai (seconds)
        self.duration = self.get_duration()

        # Da duoc thu thap chua
        self.collected = False

    def get_duration(self):
        """Tra ve thoi gian hieu luc cua power-up (giay)"""
        durations = {
            self.SHIELD: 5.0,
            self.SLOWMO: 3.0,
            self.MAGNET: 4.0,
            self.DOUBLE_POINTS: 10.0
        }
        return durations.get(self.type, 5.0)

    def move(self):
        """Di chuyen power-up sang trai"""
        self.x -= self.vel

    def update_animation(self):
        """Cap nhat hieu ung animation (float va rotate)"""
        # Float effect (len xuong)
        self.float_offset += 0.5 * self.float_direction
        if abs(self.float_offset) > 10:
            self.float_direction *= -1

        # Rotation effect
        self.rotation = (self.rotation + 2) % 360

    def draw(self, win):
        """Ve power-up len man hinh"""
        if self.img:
            # Ap dung float offset
            draw_y = self.y + self.float_offset

            # Rotate image
            rotated_img = pygame.transform.rotate(self.img, self.rotation)
            rotated_rect = rotated_img.get_rect(center=(self.x + self.width//2, draw_y + self.height//2))

            # Ve hinh
            win.blit(rotated_img, rotated_rect)

            # Ve vien sang (glow effect - optional)
            # pygame.draw.circle(win, (255, 255, 0), (int(self.x + self.width//2), int(draw_y + self.height//2)),
            #                   int(self.width//2 + 5), 2)

    def collide(self, bird):
        """
        Kiem tra va cham voi bird

        Args:
            bird: Bird object

        Returns:
            bool: True neu va cham
        """
        bird_mask = bird.get_mask()

        # Tao mask cho power-up
        if self.img:
            powerup_mask = pygame.mask.from_surface(self.img)
            offset = (self.x - bird.x, int(self.y + self.float_offset) - round(bird.y))

            # Kiem tra overlap
            point = bird_mask.overlap(powerup_mask, offset)

            if point:
                self.collected = True
                return True

        return False

    def is_off_screen(self):
        """Kiem tra power-up da ra khoi man hinh chua"""
        return self.x + self.width < 0


class PowerUpManager:
    """Quan ly tat ca power-ups trong game"""

    def __init__(self):
        self.powerups = []
        self.spawn_timer = 0
        self.spawn_interval = 300  # Spawn moi 300 frames (~5 giay)
        self.max_powerups = 2  # Toi da 2 power-ups cung luc

    def update(self, score):
        """
        Cap nhat power-ups

        Args:
            score: Diem hien tai (de tang spawn rate)
        """
        # Tang spawn rate theo diem
        adjusted_interval = max(200, self.spawn_interval - score * 2)

        # Spawn power-up moi
        self.spawn_timer += 1
        if self.spawn_timer >= adjusted_interval and len(self.powerups) < self.max_powerups:
            if random.random() < 0.3:  # 30% co hoi spawn
                self.spawn_powerup()
            self.spawn_timer = 0

        # Cap nhat tat ca power-ups
        for powerup in self.powerups[:]:
            powerup.move()
            powerup.update_animation()

            # Xoa power-up ra khoi man hinh
            if powerup.is_off_screen() or powerup.collected:
                self.powerups.remove(powerup)

    def spawn_powerup(self):
        """Tao power-up moi o vi tri random"""
        x = 600  # Bat dau tu ben phai man hinh
        y = random.randint(100, 600)  # Random height
        powerup = PowerUp(x, y)
        self.powerups.append(powerup)

    def draw(self, win):
        """Ve tat ca power-ups"""
        for powerup in self.powerups:
            powerup.draw(win)

    def check_collisions(self, bird):
        """
        Kiem tra va cham voi bird

        Args:
            bird: Bird object

        Returns:
            PowerUp hoac None: Power-up duoc thu thap
        """
        for powerup in self.powerups:
            if powerup.collide(bird):
                return powerup
        return None

    def clear(self):
        """Xoa tat ca power-ups"""
        self.powerups.clear()
        self.spawn_timer = 0


class ActivePowerUp:
    """Quan ly power-up dang active tren bird"""

    def __init__(self, powerup_type, duration):
        self.type = powerup_type
        self.duration = duration
        self.time_left = duration
        self.active = True

    def update(self, dt=1/60):
        """
        Cap nhat thoi gian con lai

        Args:
            dt: Delta time (seconds)
        """
        self.time_left -= dt
        if self.time_left <= 0:
            self.active = False

    def is_active(self):
        """Kiem tra power-up con active khong"""
        return self.active

    def get_time_percent(self):
        """Tra ve % thoi gian con lai"""
        return self.time_left / self.duration if self.duration > 0 else 0


# Test
if __name__ == "__main__":
    print("Power-up System Test")
    print("=" * 50)

    # Test tao power-ups
    PowerUp.load_images()

    print("\n1. Tao power-ups:")
    shield = PowerUp(100, 200, PowerUp.SHIELD)
    print(f"   Shield: duration={shield.duration}s")

    slowmo = PowerUp(150, 250, PowerUp.SLOWMO)
    print(f"   Slowmo: duration={slowmo.duration}s")

    magnet = PowerUp(200, 300, PowerUp.MAGNET)
    print(f"   Magnet: duration={magnet.duration}s")

    double = PowerUp(250, 350, PowerUp.DOUBLE_POINTS)
    print(f"   Double Points: duration={double.duration}s")

    print("\n2. Test PowerUpManager:")
    manager = PowerUpManager()
    print(f"   Spawn interval: {manager.spawn_interval} frames")
    print(f"   Max powerups: {manager.max_powerups}")

    print("\n3. Test ActivePowerUp:")
    active = ActivePowerUp(PowerUp.SHIELD, 5.0)
    print(f"   Active: {active.is_active()}")
    print(f"   Time percent: {active.get_time_percent() * 100:.0f}%")

    # Simulate time
    for i in range(3):
        active.update(1.0)
        print(f"   After {i+1}s: {active.time_left:.1f}s left")

    print("\nPower-up System ready!")


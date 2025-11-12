"""
Particle Effects System cho Flappy Bird
Cac hieu ung: Explosion, Stars, Trail, Dust
"""

import pygame
import random
import math
import os

class Particle:
    """Class cho mot particle don le"""

    def __init__(self, x, y, color, vel_x, vel_y, lifetime, size=3):
        self.x = x
        self.y = y
        self.color = color
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.alive = True
        self.gravity = 0.3
        self.fade = True

    def update(self):
        """Cap nhat vi tri va trang thai particle"""
        if not self.alive:
            return

        # Di chuyen
        self.x += self.vel_x
        self.y += self.vel_y

        # Ap dung gravity
        self.vel_y += self.gravity

        # Giam vel theo thoi gian (friction)
        self.vel_x *= 0.98

        # Giam lifetime
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False

    def draw(self, win):
        """Ve particle len man hinh"""
        if not self.alive:
            return

        # Tinh alpha (do trong suot)
        if self.fade:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
        else:
            alpha = 255

        # Tinh size giam dan
        current_size = max(1, int(self.size * (self.lifetime / self.max_lifetime)))

        # Tao surface trong suot
        surf = pygame.Surface((current_size * 2, current_size * 2), pygame.SRCALPHA)
        color_with_alpha = (*self.color[:3], alpha)
        pygame.draw.circle(surf, color_with_alpha, (current_size, current_size), current_size)

        # Ve len man hinh
        win.blit(surf, (int(self.x - current_size), int(self.y - current_size)))


class ParticleSystem:
    """Quan ly tat ca particles"""

    def __init__(self):
        self.particles = []

        # Load sprite images
        self.explosion_img = None
        self.star_img = None
        self._load_images()

    def _load_images(self):
        """Load particle images"""
        try:
            self.explosion_img = pygame.image.load(
                os.path.join("future_assets", "effects", "explosion.png"))
            self.star_img = pygame.image.load(
                os.path.join("future_assets", "effects", "star.png"))
            print("Particle images loaded!")
        except Exception as e:
            print(f"Could not load particle images: {e}")

    def update(self):
        """Cap nhat tat ca particles"""
        for particle in self.particles[:]:
            particle.update()
            if not particle.alive:
                self.particles.remove(particle)

    def draw(self, win):
        """Ve tat ca particles"""
        for particle in self.particles:
            particle.draw(win)

    def clear(self):
        """Xoa tat ca particles"""
        self.particles.clear()

    # ==================== EFFECT CREATORS ====================

    def create_explosion(self, x, y, color=(255, 100, 0), num_particles=20):
        """
        Tao hieu ung no

        Args:
            x, y: Vi tri
            color: Mau particles
            num_particles: So luong particles
        """
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            lifetime = random.randint(20, 40)
            size = random.randint(2, 5)

            particle = Particle(x, y, color, vel_x, vel_y, lifetime, size)
            self.particles.append(particle)

    def create_star_burst(self, x, y, num_stars=8):
        """
        Tao hieu ung sao no toa

        Args:
            x, y: Vi tri
            num_stars: So luong sao
        """
        colors = [(255, 255, 0), (255, 215, 0), (255, 255, 255)]

        for i in range(num_stars):
            angle = (2 * math.pi / num_stars) * i
            speed = random.uniform(3, 6)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            lifetime = random.randint(25, 35)
            size = random.randint(3, 6)
            color = random.choice(colors)

            particle = Particle(x, y, color, vel_x, vel_y, lifetime, size)
            self.particles.append(particle)

    def create_trail(self, x, y, color=(255, 255, 255), num_particles=3):
        """
        Tao hieu ung duoi (trail) cho bird

        Args:
            x, y: Vi tri
            color: Mau trail
            num_particles: So luong particles
        """
        for _ in range(num_particles):
            vel_x = random.uniform(-1, 1)
            vel_y = random.uniform(-1, 1)
            lifetime = random.randint(10, 20)
            size = random.randint(2, 4)

            particle = Particle(x, y, color, vel_x, vel_y, lifetime, size)
            particle.gravity = 0.1  # It gravity hon
            self.particles.append(particle)

    def create_dust(self, x, y, num_particles=5):
        """
        Tao hieu ung bui (dust) khi bird cham dat

        Args:
            x, y: Vi tri
            num_particles: So luong particles
        """
        colors = [(200, 200, 200), (150, 150, 150), (180, 180, 180)]

        for _ in range(num_particles):
            vel_x = random.uniform(-3, 3)
            vel_y = random.uniform(-5, -2)
            lifetime = random.randint(15, 25)
            size = random.randint(2, 4)
            color = random.choice(colors)

            particle = Particle(x, y, color, vel_x, vel_y, lifetime, size)
            self.particles.append(particle)

    def create_confetti(self, x, y, num_particles=30):
        """
        Tao hieu ung confetti (khi thang level)

        Args:
            x, y: Vi tri
            num_particles: So luong particles
        """
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255),
            (255, 128, 0), (128, 0, 255)
        ]

        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 10)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed - 5  # Bias len tren
            lifetime = random.randint(30, 50)
            size = random.randint(3, 6)
            color = random.choice(colors)

            particle = Particle(x, y, color, vel_x, vel_y, lifetime, size)
            self.particles.append(particle)

    def create_power_up_effect(self, x, y, powerup_type):
        """
        Tao hieu ung khi thu thap power-up

        Args:
            x, y: Vi tri
            powerup_type: Loai power-up
        """
        color_map = {
            "shield": (0, 200, 255),      # Xanh duong
            "slowmo": (200, 0, 255),      # Tim
            "magnet": (255, 215, 0),      # Vang
            "double_points": (0, 255, 0)  # Xanh la
        }

        color = color_map.get(powerup_type, (255, 255, 255))

        # Tao vong tron particles
        for i in range(16):
            angle = (2 * math.pi / 16) * i
            speed = 5
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            lifetime = 25
            size = 4

            particle = Particle(x, y, color, vel_x, vel_y, lifetime, size)
            particle.gravity = 0
            self.particles.append(particle)

    def create_score_effect(self, x, y):
        """
        Tao hieu ung khi ghi diem

        Args:
            x, y: Vi tri
        """
        colors = [(255, 255, 0), (255, 215, 0)]

        for _ in range(10):
            vel_x = random.uniform(-2, 2)
            vel_y = random.uniform(-4, -1)
            lifetime = 20
            size = 3
            color = random.choice(colors)

            particle = Particle(x, y, color, vel_x, vel_y, lifetime, size)
            particle.gravity = 0.2
            self.particles.append(particle)

    def get_particle_count(self):
        """Tra ve so luong particles hien tai"""
        return len(self.particles)


# Test
if __name__ == "__main__":
    print("Particle System Test")
    print("=" * 50)

    # Khoi tao pygame
    pygame.init()

    # Tao particle system
    ps = ParticleSystem()

    print("\n1. Test create effects:")
    ps.create_explosion(250, 400)
    print(f"   After explosion: {ps.get_particle_count()} particles")

    ps.create_star_burst(250, 400)
    print(f"   After star burst: {ps.get_particle_count()} particles")

    ps.create_trail(250, 400)
    print(f"   After trail: {ps.get_particle_count()} particles")

    ps.create_confetti(250, 400)
    print(f"   After confetti: {ps.get_particle_count()} particles")

    print("\n2. Test update:")
    for i in range(5):
        ps.update()
        print(f"   Frame {i+1}: {ps.get_particle_count()} particles alive")

    print("\n3. Test clear:")
    ps.clear()
    print(f"   After clear: {ps.get_particle_count()} particles")

    print("\nParticle System ready!")


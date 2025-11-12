"""
Flappy Bird with Breath/Voice Control
Player Mode - Control the bird using your breath or voice!
"""

import pygame
import os
import random
import sys
from breath_controller import BreathController

pygame.font.init()
pygame.mixer.init()

# Constants
WIN_WIDTH = 500
WIN_HEIGHT = 800
FPS = 30

# Load images
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# Fonts
STAT_FONT = pygame.font.SysFont("comicsans", 50)
INFO_FONT = pygame.font.SysFont("comicsans", 30)
SMALL_FONT = pygame.font.SysFont("comicsans", 20)

# Load sounds
try:
    SOUND_JUMP = pygame.mixer.Sound(os.path.join("imgs", "audio", "jump.wav"))
    SOUND_POINT = pygame.mixer.Sound(os.path.join("imgs", "audio", "point.wav"))
    SOUND_HIT = pygame.mixer.Sound(os.path.join("imgs", "audio", "hit.wav"))
    SOUND_DIE = pygame.mixer.Sound(os.path.join("imgs", "audio", "die.wav"))

    SOUND_JUMP.set_volume(0.3)
    SOUND_POINT.set_volume(0.4)
    SOUND_HIT.set_volume(0.5)
    SOUND_DIE.set_volume(0.4)
except:
    SOUND_JUMP = SOUND_POINT = SOUND_HIT = SOUND_DIE = None


class Bird:
    """Bird class for player-controlled bird"""
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        """Make the bird jump"""
        if SOUND_JUMP:
            SOUND_JUMP.play()
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def hover(self):
        """Make the bird hover (maintain altitude)"""
        # Gentle upward force to counteract gravity
        self.vel = -3

    def move(self):
        """Move the bird based on physics"""
        self.tick_count += 1

        # Calculate displacement (gravity)
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        # Limit fall speed
        if d >= 16:
            d = 16

        # Give extra boost when jumping
        if d < 0:
            d -= 2

        self.y = self.y + d

        # Handle rotation
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        """Draw the bird with animation"""
        self.img_count += 1

        # Animation cycle
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # Don't flap when falling
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        self.blit_rotate_center(win, self.img, (self.x, self.y), self.tilt)

    def blit_rotate_center(self, surf, image, topleft, angle):
        """Rotate image around center"""
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
        surf.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        """Get mask for collision detection"""
        return pygame.mask.from_surface(self.img)


class Pipe:
    """Pipe obstacle"""
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()

    def set_height(self):
        """Randomly set pipe height"""
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """Move pipe to the left"""
        self.x -= self.VEL

    def draw(self, win):
        """Draw top and bottom pipe"""
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        """Check collision with bird"""
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        return b_point or t_point


class Base:
    """Moving ground"""
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """Move ground to create scrolling effect"""
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        """Draw ground"""
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_volume_bar(win, controller):
    """Draw visual volume indicator"""
    volume = controller.get_volume()
    action = controller.get_action()

    # Bar dimensions
    bar_x = 10
    bar_y = WIN_HEIGHT - 100
    bar_width = 30
    bar_height = 80

    # Background
    pygame.draw.rect(win, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

    # Volume fill
    fill_height = int(volume * bar_height)

    # Color based on action
    if action == 'jump':
        color = (255, 0, 0)  # Red - jumping
    elif action == 'hover':
        color = (255, 255, 0)  # Yellow - hovering
    else:
        color = (100, 100, 100)  # Gray - falling

    pygame.draw.rect(win, color,
                    (bar_x, bar_y + bar_height - fill_height, bar_width, fill_height))

    # Border
    pygame.draw.rect(win, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

    # Threshold lines
    # Jump threshold (35%)
    jump_y = bar_y + int(bar_height * (1 - controller.threshold_jump))
    pygame.draw.line(win, (255, 0, 0), (bar_x, jump_y), (bar_x + bar_width, jump_y), 2)

    # Hover min threshold (15%)
    hover_y = bar_y + int(bar_height * (1 - controller.threshold_hover_min))
    pygame.draw.line(win, (255, 255, 0), (bar_x, hover_y), (bar_x + bar_width, hover_y), 1)

    # Label
    label = SMALL_FONT.render("🎤", 1, (255, 255, 255))
    win.blit(label, (bar_x, bar_y - 25))

    # Action text
    action_text = SMALL_FONT.render(action.upper(), 1, color)
    win.blit(action_text, (bar_x + 40, bar_y + 30))


def draw_game_window(win, bird, pipes, base, score, controller, show_instructions=False):
    """Draw the game window"""
    # Background
    win.blit(BG_IMG, (0, 0))

    # Pipes
    for pipe in pipes:
        pipe.draw(win)

    # Base
    base.draw(win)

    # Bird
    bird.draw(win)

    # Score
    score_text = STAT_FONT.render(f"Score: {score}", 1, (255, 255, 255))
    win.blit(score_text, (WIN_WIDTH - score_text.get_width() - 10, 10))

    # Volume bar
    draw_volume_bar(win, controller)

    # Instructions (show at start)
    if show_instructions:
        inst_bg = pygame.Surface((WIN_WIDTH - 40, 150))
        inst_bg.set_alpha(200)
        inst_bg.fill((0, 0, 0))
        win.blit(inst_bg, (20, WIN_HEIGHT // 2 - 75))

        instructions = [
            "🎤 BREATH CONTROL MODE 🎤",
            "🔊 BLOW HARD → Jump/Fly Up",
            "💨 STEADY BREATH → Hover",
            "🤐 QUIET → Fall Down",
            "Press SPACE to start!"
        ]

        for i, line in enumerate(instructions):
            text = INFO_FONT.render(line, 1, (255, 255, 255))
            win.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2,
                           WIN_HEIGHT // 2 - 60 + i * 30))

    pygame.display.update()


def show_game_over(win, score):
    """Show game over screen"""
    # Semi-transparent overlay
    overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    win.blit(overlay, (0, 0))

    # Game Over text
    game_over_font = pygame.font.SysFont("comicsans", 70)
    game_over_text = game_over_font.render("GAME OVER", 1, (255, 0, 0))
    win.blit(game_over_text, (WIN_WIDTH // 2 - game_over_text.get_width() // 2, WIN_HEIGHT // 2 - 100))

    # Final score
    score_text = STAT_FONT.render(f"Final Score: {score}", 1, (255, 255, 255))
    win.blit(score_text, (WIN_WIDTH // 2 - score_text.get_width() // 2, WIN_HEIGHT // 2))

    # Restart instructions
    restart_text = INFO_FONT.render("Press SPACE to play again", 1, (255, 255, 255))
    win.blit(restart_text, (WIN_WIDTH // 2 - restart_text.get_width() // 2, WIN_HEIGHT // 2 + 80))

    quit_text = INFO_FONT.render("Press ESC to quit", 1, (255, 255, 255))
    win.blit(quit_text, (WIN_WIDTH // 2 - quit_text.get_width() // 2, WIN_HEIGHT // 2 + 120))

    pygame.display.update()


def main():
    """Main game loop"""
    print("\n" + "="*60)
    print("🎮 FLAPPY BIRD - BREATH CONTROL EDITION 🎤")
    print("="*60)

    # Initialize window
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird - Breath Control")
    clock = pygame.time.Clock()

    # Initialize breath controller
    print("\n🎤 Initializing microphone...")
    controller = BreathController()

    print("\n📊 Calibrating...")
    controller.calibrate(duration=2.0)
    controller.start()

    print("\n✅ Ready to play!")
    print("\n💡 CONTROLS:")
    print("   🔊 Blow hard / speak loud → Bird flies up")
    print("   💨 Steady breath → Bird hovers")
    print("   🤐 Quiet / silent → Bird falls\n")

    running = True

    while running:
        # Game state
        bird = Bird(230, 350)
        pipes = [Pipe(600)]
        base = Base(730)
        score = 0
        game_started = False
        game_over = False

        # Wait for start
        waiting = True
        while waiting:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                        game_started = True
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        running = False

            draw_game_window(win, bird, pipes, base, score, controller, show_instructions=True)

        # Main game loop
        while game_started and not game_over:
            clock.tick(FPS)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_started = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_started = False
                        running = False

            # Breath control input
            action = controller.get_action()

            if action == 'jump':
                bird.jump()
            elif action == 'hover':
                bird.hover()
            # 'fall' - do nothing, let gravity work

            # Move bird
            bird.move()

            # Move base
            base.move()

            # Move pipes and check collision
            add_pipe = False
            rem_pipes = []

            for pipe in pipes:
                pipe.move()

                # Check collision
                if pipe.collide(bird):
                    if SOUND_HIT:
                        SOUND_HIT.play()
                    game_over = True

                # Remove pipes that are off screen
                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem_pipes.append(pipe)

                # Add new pipe
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            # Add new pipe
            if add_pipe:
                score += 1
                if SOUND_POINT:
                    SOUND_POINT.play()
                pipes.append(Pipe(600))

            # Remove old pipes
            for pipe in rem_pipes:
                pipes.remove(pipe)

            # Check if bird hit ground or ceiling
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                if SOUND_DIE:
                    SOUND_DIE.play()
                game_over = True

            # Draw window
            draw_game_window(win, bird, pipes, base, score, controller)

        # Game over screen
        if game_over and running:
            show_game_over(win, score)

            waiting_restart = True
            while waiting_restart:
                clock.tick(15)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting_restart = False
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            waiting_restart = False
                        if event.key == pygame.K_ESCAPE:
                            waiting_restart = False
                            running = False

    # Cleanup
    controller.stop()
    pygame.quit()
    print("\n👋 Thanks for playing!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Game interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


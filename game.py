from menu import show_menu, show_instructions
import sys
import pygame
import neat
import time
import os
import random
pygame.font.init()

# Constants
WIN_WIDTH = 500
WIN_HEIGHT = 800

GEN = 0

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

# Load backgrounds for 4 levels (with fallback to default)
BG_IMGS = []
for level in range(1, 5):
    try:
        bg = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", f"bg_level{level}.png")))
        BG_IMGS.append(bg)
        print(f"✅ Loaded bg_level{level}.png")
    except:
        # Fallback to default background if level background not found
        bg = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
        BG_IMGS.append(bg)
        print(f"⚠️  bg_level{level}.png not found, using default bg.png")

STAT_FONT = pygame.font.SysFont("comicsans", 50)

# Load sounds
try:
    pygame.mixer.init()
    SOUND_JUMP = pygame.mixer.Sound(os.path.join("imgs", "audio", "jump.wav"))
    SOUND_POINT = pygame.mixer.Sound(os.path.join("imgs", "audio", "point.wav"))
    SOUND_HIT = pygame.mixer.Sound(os.path.join("imgs", "audio", "hit.wav"))
    SOUND_DIE = pygame.mixer.Sound(os.path.join("imgs", "audio", "die.wav"))
    SOUND_SWOOSH = pygame.mixer.Sound(os.path.join("imgs", "audio", "swoosh.wav"))
    
    # Set volume
    SOUND_JUMP.set_volume(0.3)
    SOUND_POINT.set_volume(0.4)
    SOUND_HIT.set_volume(0.5)
    SOUND_DIE.set_volume(0.4)
    SOUND_SWOOSH.set_volume(0.3)
    
    # Load background music
    try:
        pygame.mixer.music.load(os.path.join("imgs", "audio", "bg_music.wav"))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)  # Loop forever
    except:
        pass
    
    print("✅ Loaded all sounds!")
except Exception as e:
    print(f"⚠️  Could not load sounds: {e}")
    SOUND_JUMP = None
    SOUND_POINT = None
    SOUND_HIT = None
    SOUND_DIE = None
    SOUND_SWOOSH = None

LEVEL_FONT = pygame.font.SysFont("comicsans", 40)

# Level settings
LEVEL_THRESHOLDS = [0, 50, 125, 250]  # Score thresholds for each level
LEVEL_NAMES = ["EASY", "MEDIUM", "HARD", "EXTREME"]
LEVEL_COLORS = [(0, 255, 0), (255, 255, 0), (255, 165, 0), (255, 0, 0)]

# Transition settings
TRANSITION_DURATION = 30  # 30 frames = 1 second at 30 fps

def get_current_level(score):
    """Determine current level based on score"""
    if score >= LEVEL_THRESHOLDS[3]:
        return 4
    elif score >= LEVEL_THRESHOLDS[2]:
        return 3
    elif score >= LEVEL_THRESHOLDS[1]:
        return 2
    else:
        return 1

def get_level_settings(level):
    """Get game settings based on level"""
    settings = {
        1: {"pipe_vel": 5, "pipe_gap": 200, "base_vel": 5},
        2: {"pipe_vel": 6, "pipe_gap": 180, "base_vel": 6},
        3: {"pipe_vel": 7, "pipe_gap": 160, "base_vel": 7},
        4: {"pipe_vel": 8, "pipe_gap": 140, "base_vel": 8}
    }
    return settings.get(level, settings[1])

# Classes
class Bird:
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
        if SOUND_JUMP:
            SOUND_JUMP.play()
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def hover(self):
        """Make the bird hover (maintain altitude) - for breath control"""
        self.vel = -3
        self.tick_count = 0

    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        # For animation of bird, loop through three images
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

        # so when bird is nose diving it isn't flapping
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    def __init__(self, x, gap=200, vel=5):
        self.x = x
        self.height = 0
        self.GAP = gap
        self.VEL = vel

        # where the top and bottom of the pipe is
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False

        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True

        return False

class Base:
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y, vel=5):
        self.y = y
        self.VEL = vel
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

def draw_window(win, birds, pipes, base, score, gen, level, show_level_up=False, transition_alpha=0, old_level=1):
    """
    Draw game window with smooth transition effect
    transition_alpha: 0-255, 0 = old background fully visible, 255 = new background fully visible
    """
    # Draw old background
    if transition_alpha > 0 and old_level != level:
        win.blit(BG_IMGS[old_level - 1], (0, 0))

        # Create a copy of new background with alpha channel for fade effect
        new_bg = BG_IMGS[level - 1].copy()
        new_bg.set_alpha(transition_alpha)
        win.blit(new_bg, (0, 0))
    else:
        # No transition, just draw current level background
        win.blit(BG_IMGS[level - 1], (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    # Draw score
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    # Draw generation
    text = STAT_FONT.render("Gen: " + str(gen), 1, (255,255,255))
    win.blit(text, (10, 10))

    # Draw level with color
    level_text = LEVEL_FONT.render(f"Level {level}: {LEVEL_NAMES[level-1]}", 1, LEVEL_COLORS[level-1])
    win.blit(level_text, (10, 70))

    # Show level up message with pulsing effect
    if show_level_up:
        level_up_font = pygame.font.SysFont("comicsans", 70)
        level_up_text = level_up_font.render(f"LEVEL {level}!", 1, LEVEL_COLORS[level-1])

        # Add glow effect by drawing shadow
        shadow_text = level_up_font.render(f"LEVEL {level}!", 1, (0, 0, 0))
        win.blit(shadow_text, (WIN_WIDTH // 2 - level_up_text.get_width() // 2 + 3, WIN_HEIGHT // 2 - 47))
        win.blit(level_up_text, (WIN_WIDTH // 2 - level_up_text.get_width() // 2, WIN_HEIGHT // 2 - 50))

    base.draw(win)
    for bird in birds:
        bird.draw(win)

    pygame.display.update()

def main(genomes, config):
    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    current_level = 1
    previous_level = 1
    old_level = 1
    level_up_timer = 0
    transition_timer = 0
    transition_alpha = 0

    run = True
    while run and len(birds) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # Update level based on score
        current_level = get_current_level(score)
        show_level_up = False

        # Check if level changed
        if current_level > previous_level:
            level_up_timer = 60  # Show level up message for 60 frames (2 seconds)
            transition_timer = TRANSITION_DURATION  # Start smooth transition
            old_level = previous_level
            previous_level = current_level
            # Update game settings
            settings = get_level_settings(current_level)
            base.VEL = settings["base_vel"]

        # Update transition alpha for smooth fade effect
        if transition_timer > 0:
            transition_alpha = int(255 * (1 - transition_timer / TRANSITION_DURATION))
            transition_timer -= 1
        else:
            transition_alpha = 0

        if level_up_timer > 0:
            show_level_up = True
            level_up_timer -= 1

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        base.move()

        # Pipes - FIXED: iterate backwards to avoid index issues
        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # FIXED: iterate backwards when removing
            for x in range(len(birds) - 1, -1, -1):
                if pipe.collide(birds[x]):
                    if SOUND_HIT:
                        SOUND_HIT.play()
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

            # Check after collision removal
            if len(birds) > 0:
                if not pipe.passed and pipe.x < birds[0].x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            if SOUND_POINT:
                SOUND_POINT.play()
            for g in ge:
                g.fitness += 5

            # Create new pipe with current level settings
            settings = get_level_settings(current_level)
            pipes.append(Pipe(WIN_WIDTH, gap=settings["pipe_gap"], vel=settings["pipe_vel"]))

        for r in rem:
            pipes.remove(r)

        # FIXED: iterate backwards to avoid index issues
        for x in range(len(birds) - 1, -1, -1):
            if birds[x].y + birds[x].img.get_height() >= 730 or birds[x].y < 0:
                if SOUND_DIE:
                    SOUND_DIE.play()
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        draw_window(win, birds, pipes, base, score, GEN, current_level, show_level_up, transition_alpha, old_level)

def play_manual_mode():
    """Chế độ người chơi thật - điều khiển bằng SPACE"""
    from database import FlappyBirdDB

    db = FlappyBirdDB()

    # Nhập tên người chơi
    screen = pygame.display.get_surface()
    player_name = get_player_name(screen)
    if not player_name:
        return

    # Setup game
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    clock = pygame.time.Clock()

    score = 0
    current_level = 1
    previous_level = 1
    max_level = 1
    level_up_timer = 0
    transition_timer = 0
    transition_alpha = 0
    old_level = 1
    game_over = False

    print(f"\n🎮 {player_name} đang chơi...")

    run = True
    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.jump()
                    if SOUND_JUMP:
                        SOUND_JUMP.play()
                if event.key == pygame.K_ESCAPE:
                    run = False

        if not game_over:
            # Update level
            current_level = get_current_level(score)
            if current_level > max_level:
                max_level = current_level

            show_level_up = False
            if current_level > previous_level:
                level_up_timer = 60
                transition_timer = TRANSITION_DURATION
                old_level = previous_level
                previous_level = current_level
                settings = get_level_settings(current_level)
                base.VEL = settings["base_vel"]

            if transition_timer > 0:
                transition_alpha = int(255 * (1 - transition_timer / TRANSITION_DURATION))
                transition_timer -= 1
            else:
                transition_alpha = 0

            if level_up_timer > 0:
                show_level_up = True
                level_up_timer -= 1

            # Move
            bird.move()
            base.move()

            # Pipes
            rem = []
            add_pipe = False
            for pipe in pipes:
                pipe.move()

                if pipe.collide(bird):
                    game_over = True
                    if SOUND_HIT:
                        SOUND_HIT.play()
                    if SOUND_DIE:
                        SOUND_DIE.play()

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

            if add_pipe:
                score += 1
                if SOUND_POINT:
                    SOUND_POINT.play()
                settings = get_level_settings(current_level)
                pipes.append(Pipe(WIN_WIDTH, gap=settings["pipe_gap"], vel=settings["pipe_vel"]))

            for r in rem:
                pipes.remove(r)

            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                game_over = True
                if SOUND_DIE:
                    SOUND_DIE.play()

        # Draw
        draw_player_window(screen, bird, pipes, base, score, current_level,
                          show_level_up, transition_alpha, old_level, game_over, player_name)

        if game_over:
            # Lưu vào database
            if db.client:
                db.save_high_score(player_name, score, max_level)
                print(f"✅ Đã lưu điểm của {player_name}: {score} điểm")

            show_game_over(screen, player_name, score, max_level, db)
            run = False

    if db.client:
        db.close()

def get_player_name(screen):
    """Nhập tên người chơi"""
    font_title = pygame.font.SysFont("comicsans", 28)
    font_input = pygame.font.SysFont("comicsans", 40)
    font_hint = pygame.font.SysFont("comicsans", 25)

    name = ""
    cursor_visible = True
    cursor_timer = 0
    clock = pygame.time.Clock()

    while True:
        clock.tick(30)
        cursor_timer += 1
        if cursor_timer >= 15:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        screen.fill((70, 130, 180))

        title = font_title.render("YOUR NAME", True, (255, 215, 0))
        screen.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 200))

        pygame.draw.rect(screen, (255, 255, 255), (50, 350, 400, 80), 3)

        name_text = font_input.render(name, True, (255, 255, 255))
        screen.blit(name_text, (70, 370))

        if cursor_visible and len(name) < 15:
            cursor_x = 70 + name_text.get_width() + 5
            pygame.draw.line(screen, (255, 255, 255), (cursor_x, 370), (cursor_x, 420), 3)

        hint1 = font_hint.render("Press ENTER to continue", True, (255, 255, 255))
        hint2 = font_hint.render("Press ESC to cancel", True, (200, 200, 200))
        screen.blit(hint1, (WIN_WIDTH // 2 - hint1.get_width() // 2, 500))
        screen.blit(hint2, (WIN_WIDTH // 2 - hint2.get_width() // 2, 550))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    return name
                elif event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 15 and event.unicode.isprintable():
                    name += event.unicode

def draw_player_window(win, bird, pipes, base, score, level, show_level_up,
                       transition_alpha, old_level, game_over, player_name):
    """Vẽ màn hình game cho người chơi"""
    if transition_alpha > 0 and old_level != level:
        win.blit(BG_IMGS[old_level - 1], (0, 0))
        new_bg = BG_IMGS[level - 1].copy()
        new_bg.set_alpha(transition_alpha)
        win.blit(new_bg, (0, 0))
    else:
        win.blit(BG_IMGS[level - 1], (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    name_font = pygame.font.SysFont("comicsans", 35)
    name_text = name_font.render(f"Player: {player_name}", 1, (255, 255, 255))
    win.blit(name_text, (10, 10))

    level_text = LEVEL_FONT.render(f"Level {level}: {LEVEL_NAMES[level-1]}", 1, LEVEL_COLORS[level-1])
    win.blit(level_text, (10, 60))

    if show_level_up:
        level_up_font = pygame.font.SysFont("comicsans", 70)
        level_up_text = level_up_font.render(f"LEVEL {level}!", 1, LEVEL_COLORS[level-1])
        shadow_text = level_up_font.render(f"LEVEL {level}!", 1, (0, 0, 0))
        win.blit(shadow_text, (WIN_WIDTH // 2 - level_up_text.get_width() // 2 + 3, WIN_HEIGHT // 2 - 47))
        win.blit(level_up_text, (WIN_WIDTH // 2 - level_up_text.get_width() // 2, WIN_HEIGHT // 2 - 50))

    base.draw(win)
    bird.draw(win)

    if game_over:
        overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        win.blit(overlay, (0, 0))

    pygame.display.update()

def show_game_over(screen, player_name, score, max_level, db):
    """Hiển thị màn hình game over"""
    font_title = pygame.font.SysFont("comicsans", 70)
    font_text = pygame.font.SysFont("comicsans", 40)
    font_small = pygame.font.SysFont("comicsans", 30)

    top_scores = []
    if db.client:
        top_scores = db.get_top_scores(5)

    screen.fill((50, 50, 50))

    title = font_title.render("GAME OVER!", True, (255, 50, 50))
    screen.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 100))

    stats = [
        f"Player: {player_name}",
        f"Score: {score}",
        f"Max Level: {max_level}"
    ]

    y = 220
    for stat in stats:
        text = font_text.render(stat, True, (255, 255, 255))
        screen.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2, y))
        y += 50

    if top_scores:
        y = 400
        top_title = font_text.render("TOP 5:", True, (255, 215, 0))
        screen.blit(top_title, (WIN_WIDTH // 2 - top_title.get_width() // 2, y))
        y += 50

        for i, s in enumerate(top_scores[:5], 1):
            score_text = font_small.render(
                f"{i}. {s['player_name']}: {s['score']} pts",
                True, (200, 200, 200)
            )
            screen.blit(score_text, (WIN_WIDTH // 2 - score_text.get_width() // 2, y))
            y += 35

    hint1 = font_small.render("Press any key to return to menu", True, (255, 255, 255))
    screen.blit(hint1, (WIN_WIDTH // 2 - hint1.get_width() // 2, WIN_HEIGHT - 80))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False



def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    
    # Show menu first
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird AI - NEAT")
    
    while True:
        choice = show_menu(screen)
        
        if choice == "exit":
            pygame.quit()
            sys.exit()
        elif choice == "help":
            cont = show_instructions(screen)
            if not cont:
                pygame.quit()
                sys.exit()
        elif choice == "start":
            run(config_path)
            # After game ends, show menu again
        else:
            break

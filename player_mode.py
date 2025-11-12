"""
Player Mode - Chế độ người chơi thật (không phải AI)
Điều khiển: SPACE để nhảy
"""
import pygame
import os
import random
from datetime import datetime

# Import từ game chính
import sys
sys.path.append(os.path.dirname(__file__))

# Constants
WIN_WIDTH = 500
WIN_HEIGHT = 800

# Import classes từ game chính
def play_manual_mode():
    """Chế độ chơi thủ công cho người"""
    from game import (
        Bird, Pipe, Base, blitRotateCenter,
        BG_IMGS, BIRD_IMGS, PIPE_IMG, BASE_IMG,
        WIN_WIDTH, WIN_HEIGHT,
        get_current_level, get_level_settings,
        STAT_FONT, LEVEL_FONT, LEVEL_NAMES, LEVEL_COLORS,
        SOUND_JUMP, SOUND_POINT, SOUND_HIT, SOUND_DIE
    )
    from database import FlappyBirdDB

    # Khởi tạo database
    db = FlappyBirdDB()

    # Nhập tên người chơi
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird - Player Mode")

    player_name = get_player_name(screen)
    if not player_name:
        return  # User cancelled

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

    start_time = datetime.now()
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
                if event.key == pygame.K_RETURN and game_over:
                    # Restart
                    return play_manual_mode()

        if not game_over:
            # Update level
            current_level = get_current_level(score)
            if current_level > max_level:
                max_level = current_level

            show_level_up = False
            if current_level > previous_level:
                level_up_timer = 60
                transition_timer = 30
                old_level = previous_level
                previous_level = current_level
                settings = get_level_settings(current_level)
                base.VEL = settings["base_vel"]

            if transition_timer > 0:
                transition_alpha = int(255 * (1 - transition_timer / 30))
                transition_timer -= 1
            else:
                transition_alpha = 0

            if level_up_timer > 0:
                show_level_up = True
                level_up_timer -= 1

            # Move bird
            bird.move()

            # Move base
            base.move()

            # Pipes
            rem = []
            add_pipe = False
            for pipe in pipes:
                pipe.move()

                # Check collision
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

            # Check ground/ceiling collision
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                game_over = True
                if SOUND_DIE:
                    SOUND_DIE.play()

        # Draw
        draw_player_window(screen, bird, pipes, base, score, current_level,
                          show_level_up, transition_alpha, old_level, game_over, player_name)

        # Game over
        if game_over and run:
            end_time = datetime.now()

            # Lưu vào database
            if db.client:
                db.save_high_score(player_name, score, max_level)
                print(f"✅ Đã lưu điểm của {player_name}: {score} điểm")

            # Show game over screen
            show_game_over(screen, player_name, score, max_level, db)

            # Wait for restart or exit
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            # Restart
                            return play_manual_mode()
                        if event.key == pygame.K_ESCAPE:
                            waiting = False
                            run = False

    # Close database
    if db.client:
        db.close()

    pygame.quit()

def get_player_name(screen):
    """Nhập tên người chơi"""
    font_title = pygame.font.SysFont("comicsans", 60)
    font_input = pygame.font.SysFont("comicsans", 50)
    font_hint = pygame.font.SysFont("comicsans", 30)

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

        # Title
        title = font_title.render("ENTER YOUR NAME", True, (255, 215, 0))
        screen.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 200))

        # Input box
        pygame.draw.rect(screen, (255, 255, 255), (50, 350, 400, 80), 3)

        # Name text
        name_text = font_input.render(name, True, (255, 255, 255))
        screen.blit(name_text, (70, 370))

        # Cursor
        if cursor_visible and len(name) < 15:
            cursor_x = 70 + name_text.get_width() + 5
            pygame.draw.line(screen, (255, 255, 255), (cursor_x, 370), (cursor_x, 420), 3)

        # Hint
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
    from game import BG_IMGS, LEVEL_NAMES, LEVEL_COLORS, STAT_FONT, LEVEL_FONT

    # Draw background with transition
    if transition_alpha > 0 and old_level != level:
        win.blit(BG_IMGS[old_level - 1], (0, 0))
        new_bg = BG_IMGS[level - 1].copy()
        new_bg.set_alpha(transition_alpha)
        win.blit(new_bg, (0, 0))
    else:
        win.blit(BG_IMGS[level - 1], (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    # Draw score
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    # Draw player name
    name_font = pygame.font.SysFont("comicsans", 35)
    name_text = name_font.render(f"Player: {player_name}", 1, (255, 255, 255))
    win.blit(name_text, (10, 10))

    # Draw level
    level_text = LEVEL_FONT.render(f"Level {level}: {LEVEL_NAMES[level-1]}", 1, LEVEL_COLORS[level-1])
    win.blit(level_text, (10, 60))

    # Show level up
    if show_level_up:
        level_up_font = pygame.font.SysFont("comicsans", 70)
        level_up_text = level_up_font.render(f"LEVEL {level}!", 1, LEVEL_COLORS[level-1])
        shadow_text = level_up_font.render(f"LEVEL {level}!", 1, (0, 0, 0))
        win.blit(shadow_text, (WIN_WIDTH // 2 - level_up_text.get_width() // 2 + 3, WIN_HEIGHT // 2 - 47))
        win.blit(level_up_text, (WIN_WIDTH // 2 - level_up_text.get_width() // 2, WIN_HEIGHT // 2 - 50))

    base.draw(win)
    bird.draw(win)

    # Game over overlay
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

    # Get top scores
    top_scores = []
    if db.client:
        top_scores = db.get_top_scores(5)

    screen.fill((50, 50, 50))

    # Title
    title = font_title.render("GAME OVER!", True, (255, 50, 50))
    screen.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 100))

    # Player stats
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

    # Top scores
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

    # Hints
    hint1 = font_small.render("Press ENTER to play again", True, (255, 255, 255))
    hint2 = font_small.render("Press ESC to exit", True, (200, 200, 200))
    screen.blit(hint1, (WIN_WIDTH // 2 - hint1.get_width() // 2, WIN_HEIGHT - 100))
    screen.blit(hint2, (WIN_WIDTH // 2 - hint2.get_width() // 2, WIN_HEIGHT - 60))

    pygame.display.update()

if __name__ == "__main__":
    play_manual_mode()


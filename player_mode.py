"""
Player Mode - Che do nguoi choi that (khong phai AI)
Dieu khien: SPACE de nhay
"""
import pygame
import os
import random
from datetime import datetime

# Constants
WIN_WIDTH = 500
WIN_HEIGHT = 800

# ============= DINH NGHIA HAM TRUOC =============

def get_player_name(screen):
    """Nhap ten nguoi choi"""
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

# ============= HAM CHINH CHOI GAME =============

def play_manual_mode():
    """Che do choi thu cong cho nguoi"""
    from game import (
        Bird, Pipe, Base,
        BG_IMGS, WIN_WIDTH, WIN_HEIGHT,
        get_current_level, get_level_settings,
        STAT_FONT, LEVEL_FONT, LEVEL_NAMES, LEVEL_COLORS,
        SOUND_JUMP, SOUND_POINT, SOUND_HIT, SOUND_DIE
    )
    
    try:
        from database import FlappyBirdDB
        db = FlappyBirdDB()
    except:
        db = None
        print("Database khong khoi tao duoc, van choi binh thuong")

    # Nhap ten nguoi choi
    pygame.init()
    screen = pygame.display.get_surface()
    if screen is None:
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
    game_over = False

    print(f"\nNguoi choi: {player_name} dang choi...")

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

            if current_level > previous_level:
                level_up_timer = 60
                previous_level = current_level
                settings = get_level_settings(current_level)
                base.VEL = settings["base_vel"]

            # Move
            bird.move()
            base.move()

            # Add pipes
            add_pipe = False
            rem = []
            for pipe in pipes:
                if not game_over:
                    if pipe.collide(bird):
                        game_over = True
                        if SOUND_HIT:
                            SOUND_HIT.play()

                    if not pipe.passed and pipe.x < bird.x:
                        pipe.passed = True
                        add_pipe = True

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

                pipe.move()

            if add_pipe:
                score += 1
                pipes.append(Pipe(600))
                if SOUND_POINT:
                    SOUND_POINT.play()

            for r in rem:
                pipes.remove(r)

            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                game_over = True
                if SOUND_DIE:
                    SOUND_DIE.play()

        # Draw
        win = screen
        win.blit(BG_IMGS[current_level - 1], (0, 0))

        for pipe in pipes:
            pipe.draw(win)

        base.draw(win)
        bird.draw(win)

        # Score
        text = STAT_FONT.render(f"Score: {score}", 1, (255, 255, 255))
        win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

        # Level
        level_name = LEVEL_NAMES.get(current_level, f"Level {current_level}")
        level_color = LEVEL_COLORS.get(current_level, (255, 255, 255))
        level_text = LEVEL_FONT.render(level_name, 1, level_color)
        win.blit(level_text, (10, 10))

        # Level up message
        if level_up_timer > 0:
            font_big = pygame.font.SysFont("comicsans", 70)
            levelup_text = font_big.render("LEVEL UP!", 1, (255, 215, 0))
            win.blit(levelup_text, (WIN_WIDTH // 2 - levelup_text.get_width() // 2, WIN_HEIGHT // 2 - 100))
            level_up_timer -= 1

        # Game over
        if game_over:
            font_big = pygame.font.SysFont("comicsans", 70)
            gameover_text = font_big.render("GAME OVER", 1, (255, 0, 0))
            win.blit(gameover_text, (WIN_WIDTH // 2 - gameover_text.get_width() // 2, WIN_HEIGHT // 2 - 100))

            font_small = pygame.font.SysFont("comicsans", 35)
            score_text = font_small.render(f"Final Score: {score}", 1, (255, 255, 255))
            win.blit(score_text, (WIN_WIDTH // 2 - score_text.get_width() // 2, WIN_HEIGHT // 2))

            restart_text = font_small.render("Press ENTER to restart", 1, (200, 200, 200))
            win.blit(restart_text, (WIN_WIDTH // 2 - restart_text.get_width() // 2, WIN_HEIGHT // 2 + 50))

            esc_text = font_small.render("Press ESC to exit", 1, (150, 150, 150))
            win.blit(esc_text, (WIN_WIDTH // 2 - esc_text.get_width() // 2, WIN_HEIGHT // 2 + 100))

            # Save to database
            if db and db.client:
                try:
                    db.save_high_score(player_name, score, max_level)
                except:
                    pass

        pygame.display.update()

    # Cleanup
    if db and db.client:
        db.close()

    print(f"\nGame ket thuc! Score: {score}")


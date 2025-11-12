"""
Che do PLAY tich hop - Vua dung SPACE vua dung hoi tho
"""
import pygame
import sys

def play_hybrid_mode():
    """Che do choi ket hop SPACE va HOI THO"""
    try:
        from game import (
            Bird, Pipe, Base, BG_IMGS, WIN_WIDTH, WIN_HEIGHT,
            get_current_level, get_level_settings, TRANSITION_DURATION,
            STAT_FONT, LEVEL_FONT, LEVEL_NAMES, LEVEL_COLORS,
            SOUND_JUMP, SOUND_POINT, SOUND_HIT, SOUND_DIE,
            get_player_name, show_game_over
        )
        from database import FlappyBirdDB
    except Exception as e:
        print(f"LOI IMPORT: {e}")
        import traceback
        traceback.print_exc()
        return

    # Khoi tao breath controller (neu co)
    breath_available = False
    controller = None

    try:
        from breath_controller import BreathController
        controller = BreathController()
        breath_available = True
        print("Breath controller: ON")
    except Exception as e:
        print(f"Breath controller: OFF (chi dung SPACE)")

    db = FlappyBirdDB()
    screen = pygame.display.get_surface()
    
    # Dam bao screen luon ton tai
    if screen is None:
        screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Flappy Bird - Player Mode")
        print("Da tao pygame screen moi")

    player_name = get_player_name(screen)
    if not player_name:
        print("Nguoi choi huy nhap ten")
        return

    # Calibrate neu co breath controller
    if breath_available and controller:
        show_calibration_screen(screen, WIN_WIDTH, WIN_HEIGHT)
        controller.calibrate(duration=2.0)
        controller.start()
        print(f"{player_name} dang choi: SPACE + HOI THO")
    else:
        print(f"{player_name} dang choi: SPACE only")

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

    print(f"Game bat dau! Player: {player_name}")

    run = True
    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.jump()
                if event.key == pygame.K_ESCAPE:
                    run = False

        if not game_over:
            # BREATH CONTROL (neu co)
            if breath_available and controller:
                action = controller.get_action()
                if action == 'jump':
                    bird.jump()
                elif action == 'hover':
                    bird.hover()

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

            bird.move()
            base.move()

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
        try:
            if breath_available and controller:
                draw_hybrid_window(screen, bird, pipes, base, score, current_level,
                                 show_level_up, transition_alpha, old_level,
                                 game_over, player_name, controller,
                                 BG_IMGS, WIN_WIDTH, WIN_HEIGHT, STAT_FONT, LEVEL_FONT, LEVEL_NAMES, LEVEL_COLORS)
            else:
                draw_player_window(screen, bird, pipes, base, score, current_level,
                                 show_level_up, transition_alpha, old_level,
                                 game_over, player_name,
                                 BG_IMGS, WIN_WIDTH, WIN_HEIGHT, STAT_FONT, LEVEL_FONT, LEVEL_NAMES, LEVEL_COLORS)
        except Exception as e:
            print(f"LOI VE: {e}")
            import traceback
            traceback.print_exc()

        if game_over:
            if db.client:
                db.save_high_score(player_name, score, max_level)
                print(f"Da luu diem cua {player_name}: {score} diem")
            show_game_over(screen, player_name, score, max_level, db)
            run = False

    if breath_available and controller:
        controller.stop()
    if db.client:
        db.close()

    print("Tro ve menu...")

def show_calibration_screen(screen, WIN_WIDTH, WIN_HEIGHT):
    """Hien thi man hinh calibration"""
    font_title = pygame.font.SysFont("comicsans", 24)
    font_text = pygame.font.SysFont("comicsans", 22)

    screen.fill((70, 130, 180))

    title = font_title.render("CALIBRATING MIC", True, (255, 215, 0))
    screen.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 250))

    text1 = font_text.render("Stay quiet for 2 seconds...", True, (255, 255, 255))
    screen.blit(text1, (WIN_WIDTH // 2 - text1.get_width() // 2, 350))

    pygame.display.update()

def draw_player_window(win, bird, pipes, base, score, level, show_level_up,
                       transition_alpha, old_level, game_over, player_name,
                       BG_IMGS, WIN_WIDTH, WIN_HEIGHT, STAT_FONT, LEVEL_FONT, LEVEL_NAMES, LEVEL_COLORS):
    """Ve man hinh game binh thuong (khong co breath bar)"""
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

    name_font = pygame.font.SysFont("comicsans", 28)
    name_text = name_font.render(f"Player: {player_name}", 1, (255, 255, 255))
    win.blit(name_text, (10, 10))

    level_text = LEVEL_FONT.render(f"Level {level}: {LEVEL_NAMES[level-1]}", 1, LEVEL_COLORS[level-1])
    win.blit(level_text, (10, 60))

    if show_level_up:
        level_up_font = pygame.font.SysFont("comicsans", 50)
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

def draw_hybrid_window(win, bird, pipes, base, score, level, show_level_up,
                      transition_alpha, old_level, game_over, player_name, controller,
                      BG_IMGS, WIN_WIDTH, WIN_HEIGHT, STAT_FONT, LEVEL_FONT, LEVEL_NAMES, LEVEL_COLORS):
    """Ve man hinh game voi breath indicator"""
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

    name_font = pygame.font.SysFont("comicsans", 28)
    name_text = name_font.render(f"Player: {player_name}", 1, (255, 215, 0))
    win.blit(name_text, (10, 10))

    level_text = LEVEL_FONT.render(f"Level {level}: {LEVEL_NAMES[level-1]}", 1, LEVEL_COLORS[level-1])
    win.blit(level_text, (10, 60))

    # Draw volume bar
    draw_volume_indicator(win, controller, WIN_HEIGHT)

    if show_level_up:
        level_up_font = pygame.font.SysFont("comicsans", 50)
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

def draw_volume_indicator(win, controller, WIN_HEIGHT):
    """Ve thanh volume"""
    volume = controller.get_volume()
    action = controller.get_action()

    bar_x = 10
    bar_y = WIN_HEIGHT - 120
    bar_width = 35
    bar_height = 100

    pygame.draw.rect(win, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))

    fill_height = int(volume * bar_height)

    if action == 'jump':
        color = (255, 50, 50)
    elif action == 'hover':
        color = (255, 255, 0)
    else:
        color = (100, 100, 100)

    pygame.draw.rect(win, color,
                    (bar_x, bar_y + bar_height - fill_height, bar_width, fill_height))

    pygame.draw.rect(win, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

    jump_y = bar_y + int(bar_height * (1 - controller.threshold_jump))
    pygame.draw.line(win, (255, 0, 0), (bar_x, jump_y), (bar_x + bar_width, jump_y), 2)

    hover_y = bar_y + int(bar_height * (1 - controller.threshold_hover_min))
    pygame.draw.line(win, (255, 255, 0), (bar_x, hover_y), (bar_x + bar_width, hover_y), 1)

    small_font = pygame.font.SysFont("comicsans", 16)
    action_text = small_font.render(action.upper(), 1, color)
    win.blit(action_text, (bar_x + 45, bar_y + 40))


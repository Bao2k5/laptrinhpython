"""
Breath Control Functions for Game.py
Chứa các hàm để tích hợp breath control vào game chính
"""
import pygame
from game import (
    Bird, Pipe, Base, BG_IMGS, WIN_WIDTH, WIN_HEIGHT,
    get_current_level, get_level_settings, TRANSITION_DURATION,
    STAT_FONT, LEVEL_FONT, LEVEL_NAMES, LEVEL_COLORS,
    SOUND_JUMP, SOUND_POINT, SOUND_HIT, SOUND_DIE
)

def play_breath_mode():
    """Chế độ chơi bằng hơi thở / giọng nói"""
    try:
        from breath_controller import BreathController
    except ImportError:
        print("❌ Không tìm thấy breath_controller.py!")
        print("💡 Vui lòng đảm bảo file breath_controller.py có trong thư mục.")

        # Show error on screen
        screen = pygame.display.get_surface()
        font = pygame.font.SysFont("comicsans", 40)
        screen.fill((70, 130, 180))

        error1 = font.render("❌ Missing breath_controller.py", True, (255, 50, 50))
        error2 = font.render("Press any key to return...", True, (255, 255, 255))

        screen.blit(error1, (WIN_WIDTH // 2 - error1.get_width() // 2, 300))
        screen.blit(error2, (WIN_WIDTH // 2 - error2.get_width() // 2, 400))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    waiting = False
        return

    from database import FlappyBirdDB
    from game import get_player_name, show_game_over

    db = FlappyBirdDB()

    # Nhập tên người chơi
    screen = pygame.display.get_surface()
    player_name = get_player_name(screen)
    if not player_name:
        return

    # Khởi tạo breath controller
    print("\n🎤 Khởi tạo điều khiển bằng hơi thở...")
    controller = BreathController()

    # Calibration screen
    show_calibration_screen(screen)
    controller.calibrate(duration=2.0)
    controller.start()

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

    print(f"\n🎮 {player_name} đang chơi với breath control...")
    print("💨 Thổi mạnh = Bay cao | Thở đều = Giữ độ cao | Im lặng = Rơi xuống")

    run = True
    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        if not game_over:
            # BREATH CONTROL INPUT
            action = controller.get_action()

            if action == 'jump':
                bird.jump()
            elif action == 'hover':
                bird.hover()
            # 'fall' - không làm gì, để trọng lực kéo xuống

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

        # Draw với volume bar
        draw_breath_player_window(screen, bird, pipes, base, score, current_level,
                                  show_level_up, transition_alpha, old_level,
                                  game_over, player_name, controller)

        if game_over:
            # Lưu vào database
            if db.client:
                db.save_high_score(f"{player_name} 🎤", score, max_level)
                print(f"✅ Đã lưu điểm của {player_name}: {score} điểm (Breath Mode)")

            show_game_over(screen, f"{player_name} 🎤", score, max_level, db)
            run = False

    controller.stop()
    if db.client:
        db.close()

def show_calibration_screen(screen):
    """Hiển thị màn hình calibration"""
    font_title = pygame.font.SysFont("comicsans", 50)
    font_text = pygame.font.SysFont("comicsans", 35)

    screen.fill((70, 130, 180))

    title = font_title.render("🎤 CALIBRATING MICROPHONE", True, (255, 215, 0))
    screen.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 250))

    text1 = font_text.render("Please stay QUIET for 2 seconds...", True, (255, 255, 255))
    screen.blit(text1, (WIN_WIDTH // 2 - text1.get_width() // 2, 350))

    text2 = font_text.render("🤫", True, (255, 255, 255))
    screen.blit(text2, (WIN_WIDTH // 2 - text2.get_width() // 2, 420))

    pygame.display.update()

def draw_breath_player_window(win, bird, pipes, base, score, level, show_level_up,
                               transition_alpha, old_level, game_over, player_name, controller):
    """Vẽ màn hình game với breath control indicator"""
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
    name_text = name_font.render(f"🎤 {player_name}", 1, (255, 215, 0))
    win.blit(name_text, (10, 10))

    level_text = LEVEL_FONT.render(f"Level {level}: {LEVEL_NAMES[level-1]}", 1, LEVEL_COLORS[level-1])
    win.blit(level_text, (10, 60))

    # Draw volume bar
    draw_volume_indicator(win, controller)

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

def draw_volume_indicator(win, controller):
    """Vẽ thanh volume indicator"""
    volume = controller.get_volume()
    action = controller.get_action()

    # Bar dimensions
    bar_x = 10
    bar_y = WIN_HEIGHT - 120
    bar_width = 35
    bar_height = 100

    # Background
    pygame.draw.rect(win, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))

    # Volume fill
    fill_height = int(volume * bar_height)

    # Color based on action
    if action == 'jump':
        color = (255, 50, 50)  # Red
    elif action == 'hover':
        color = (255, 255, 0)  # Yellow
    else:
        color = (100, 100, 100)  # Gray

    pygame.draw.rect(win, color,
                    (bar_x, bar_y + bar_height - fill_height, bar_width, fill_height))

    # Border
    pygame.draw.rect(win, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

    # Threshold lines
    jump_y = bar_y + int(bar_height * (1 - controller.threshold_jump))
    pygame.draw.line(win, (255, 0, 0), (bar_x, jump_y), (bar_x + bar_width, jump_y), 2)

    hover_y = bar_y + int(bar_height * (1 - controller.threshold_hover_min))
    pygame.draw.line(win, (255, 255, 0), (bar_x, hover_y), (bar_x + bar_width, hover_y), 1)

    # Icon and action text
    small_font = pygame.font.SysFont("comicsans", 18)
    icon_text = small_font.render("🎤", 1, (255, 255, 255))
    win.blit(icon_text, (bar_x, bar_y - 25))

    action_text = small_font.render(action.upper(), 1, color)
    win.blit(action_text, (bar_x + 45, bar_y + 40))


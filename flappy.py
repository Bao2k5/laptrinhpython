import pygame
import random
import json
import os
import sys
from AI.genetic import next_generation
from AI.bird_ai import BirdAI
from AI.model_io import save_model, load_model

pygame.init()
PLAYER_SCORE_FILE = "player_scores.json"
WIDTH = 500
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Python")

paused = False
high_score = 0

bg_img = pygame.image.load("assets/background.png")
bird_img = pygame.image.load("assets/bird.png")
pipe_img = pygame.image.load("assets/pipe.png")
menu_bg = pygame.image.load("assets/menu_bg.png")
gameover_bg = pygame.image.load("assets/gameover_bg.png")
play_btn = pygame.image.load("assets/play_btn.png")
play_btn_hover = pygame.image.load("assets/play_btn_hover.png")
train_btn = pygame.image.load("assets/train_btn.png")
train_btn_hover = pygame.image.load("assets/train_btn_hover.png")
quit_btn = pygame.image.load("assets/quit_btn.png")
quit_btn_hover = pygame.image.load("assets/quit_btn_hover.png")

bird_img = pygame.transform.scale(bird_img, (40, 30))
pipe_img = pygame.transform.scale(pipe_img, (80, 500))
pipe_top_img = pygame.transform.flip(pipe_img, False, True)
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
gameover_bg = pygame.transform.scale(gameover_bg, (WIDTH, HEIGHT))

btn_width, btn_height = 200, 50
play_btn = pygame.transform.scale(play_btn, (btn_width, btn_height))
play_btn_hover = pygame.transform.scale(play_btn_hover, (btn_width, btn_height))
train_btn = pygame.transform.scale(train_btn, (btn_width, btn_height))
train_btn_hover = pygame.transform.scale(train_btn_hover, (btn_width, btn_height))
quit_btn = pygame.transform.scale(quit_btn, (btn_width, btn_height))
quit_btn_hover = pygame.transform.scale(quit_btn_hover, (btn_width, btn_height))

flap_sound = pygame.mixer.Sound("assets/flap.wav")
hit_sound = pygame.mixer.Sound("assets/hit.wav")

bird = pygame.Rect(50, 300, 40, 30)
bird_speed = 0
gravity = 0.4
jump_force = -7

pipe_width = 80
pipe_gap = 150
pipe_x = WIDTH
pipe_height = random.randint(100, 350)
pipe_speed = 3
level = 1
score_to_level_up = 20

score = 0

clock = pygame.time.Clock()
running = True

def load_highscore():
    if not os.path.exists(PLAYER_SCORE_FILE):
        save_highscore({})
        return {}

    try:
        with open(PLAYER_SCORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except:
        print("⚠ player_scores.json bị hỏng → tạo file mới")
        save_highscore({})
        return {}

def save_highscore(data):
    sorted_scores = dict(
        sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]
    )

    with open(PLAYER_SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def draw_button(rect, text, mouse_pos, color, hover_color):
    font = pygame.font.Font(None, 40)
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect)
    else:
        pygame.draw.rect(screen, color, rect)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(rect.x + rect.width//2, rect.y + rect.height//2))
    screen.blit(text_surf, text_rect)

def draw_button_with_text(image, image_hover, rect, mouse_pos, text):
    font = pygame.font.Font(None, 40)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(rect.x + rect.width // 2, rect.y + rect.height // 2))

    if rect.collidepoint(mouse_pos):
        screen.blit(image_hover, rect)
    else:
        screen.blit(image, rect)

    screen.blit(text_surf, text_rect)

def main_menu():
    play_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 60, btn_width, btn_height)
    train_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 10, btn_width, btn_height)
    highscore_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, btn_width, btn_height)
    quit_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 160, btn_width, btn_height)

    font_title = pygame.font.Font(None, 80)

    while True:
        screen.blit(menu_bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        title_text = font_title.render("FLAPPY BIRD", True, (255, 255, 0))
        screen.blit(title_text, (WIDTH // 2 - 200, HEIGHT // 2 - 180))

        # Play
        draw_button_with_text(play_btn, play_btn_hover, play_rect, mouse_pos, "Play")
        if play_rect.collidepoint(mouse_pos) and mouse_click:
            player_name = input_player_name()
            return ("play", player_name)

        # Train
        draw_button_with_text(train_btn, train_btn_hover, train_rect, mouse_pos, "TrainAI")
        if train_rect.collidepoint(mouse_pos) and mouse_click:
            return ("train", None)

        draw_button_with_text(play_btn, play_btn_hover, play_rect, mouse_pos, "Play")
        draw_button_with_text(train_btn, train_btn_hover, train_rect, mouse_pos, "TrainAI")
        draw_button_with_text(quit_btn, quit_btn_hover, quit_rect, mouse_pos, "Quit")

        draw_button_with_text(play_btn, play_btn_hover, highscore_rect, mouse_pos, "Scores")
        if highscore_rect.collidepoint(mouse_pos) and mouse_click:
            return ("scores", None)

        # Quit
        draw_button_with_text(quit_btn, quit_btn_hover, quit_rect, mouse_pos, "Quit")
        if quit_rect.collidepoint(mouse_pos) and mouse_click:
            pygame.quit()
            sys.exit()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def input_player_name():
    font = pygame.font.Font(None, 50)
    name = ""
    input_active = True

    while input_active:
        screen.fill((20, 20, 30))

        text = font.render("Enter Your Name:", True, (255, 255, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 180))

        name_surface = font.render(name, True, (255, 255, 255))
        pygame.draw.rect(screen, (100, 100, 100), (WIDTH // 2 - 150, 250, 300, 60))
        screen.blit(name_surface, (WIDTH // 2 - 140, 260))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if len(name.strip()) > 0:
                        return name

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 12:
                        name += event.unicode

def play_normal_game(player_name):
    global bird_speed, high_score, paused, highscores  # thêm highscores để sửa dict không lỗi

    bird = pygame.Rect(50, 300, 40, 30)
    bird_speed = 0
    pipe_x = WIDTH
    pipe_height = random.randint(100, 350)
    pipe_speed = 3
    score = 0
    level = 1
    paused = False

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        # -------- EVENT --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    paused = not paused

                if event.key == pygame.K_SPACE:
                    if paused:
                        paused = False
                    bird_speed = jump_force
                    flap_sound.play()

        # -------- PAUSE SCREEN --------
        if paused:
            screen.blit(bg_img, (0, 0))
            screen.blit(bird_img, bird)

            font_big = pygame.font.Font(None, 70)
            pause_text = font_big.render("PAUSED", True, (255, 255, 0))
            screen.blit(pause_text, (WIDTH // 2 - 120, HEIGHT // 2 - 60))

            font_small = pygame.font.Font(None, 40)
            resume_text = font_small.render("Press SPACE to resume", True, (255, 255, 255))
            screen.blit(resume_text, (WIDTH // 2 - 180, HEIGHT // 2 + 10))

            pygame.display.update()
            continue

        # -------- UPDATE --------
        bird_speed += gravity
        bird.y += int(bird_speed)

        pipe_x -= pipe_speed

        if pipe_x < -pipe_width:
            pipe_x = WIDTH
            pipe_height = random.randint(100, 350)
            score += 1

            if score % score_to_level_up == 0:
                level += 1
                pipe_speed += 0.7

        pipe_top = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
        pipe_bottom = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT)

        if bird.colliderect(pipe_top) or bird.colliderect(pipe_bottom) or bird.y < 0 or bird.y > HEIGHT:
            hit_sound.play()

            scores = load_highscore()
            player_best = scores.get(player_name, 0)

            if score > player_best:
                scores[player_name] = score
                save_highscore(scores)

            action = game_over_menu(score, player_highscore, player_name)

            if action == "restart":
                return play_normal_game(player_name)

            elif action == "menu":
                return score

            elif action == "quit":
                pygame.quit()
                sys.exit()

        screen.blit(bg_img, (0, 0))
        screen.blit(bird_img, bird)

        screen.blit(pipe_top_img, (pipe_x, pipe_height - 500))
        screen.blit(pipe_img, (pipe_x, pipe_height + pipe_gap))

        font = pygame.font.Font(None, 40)

        name_text = font.render(f"Player: {player_name}", True, (255, 255, 255))
        screen.blit(name_text, (WIDTH - 200, 10))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        lvl_text = font.render(f"Level: {level}", True, (255, 255, 0))
        screen.blit(lvl_text, (10, 50))

        player_highscore = highscores.get(player_name, 0)
        if score > player_highscore:
            player_highscore = score

        high_text = font.render(f"HighScore: {player_highscore}", True, (255, 215, 0))
        screen.blit(high_text, (10, 90))

        pygame.display.update()

def save_ai_metadata(generation, best_score):
    data = {
        "generation": generation,
        "best_score": best_score
    }
    with open("ai_metadata.json", "w") as f:
        json.dump(data, f)

def load_ai_metadata():
    filename = "ai_metadata.json"

    if not os.path.exists(filename):
        save_ai_metadata(1, 0)
        return {"generation": 1, "best_score": 0}

    try:
        with open(filename, "r") as f:
            data = json.load(f)

        if "generation" not in data or "best_score" not in data:
            return {"generation": 1, "best_score": 0}

        return data

    except (json.JSONDecodeError, ValueError):
        print("ai_metadata.json is corrupted or empty → Resetting metadata.")
        return {"generation": 1, "best_score": 0}
    
def train_ai():
    population = 50
    max_generation = 5

    # ----- LOAD METADATA -----
    metadata = load_ai_metadata()
    generation = metadata["generation"]
    best_score_display = metadata["best_score"]

    # ----- LOAD BEST MODEL -----
    loaded_brain = load_model()
    if loaded_brain is not None:
        print("Loaded AI model from file!")
        birds = [BirdAI(loaded_brain) for _ in range(population)]
    else:
        birds = [BirdAI() for _ in range(population)]

    pipes = []
    frame = 0
    pipe_spawn_time = 120
    pipe_speed = 3
    game_score = 0

    font = pygame.font.Font(None, 40)
    stop_rect = pygame.Rect(WIDTH - 120, 10, 110, 40)

    while True:

        # ============================
        #   CHECK MAX GENERATION
        # ============================
        if generation > max_generation:
            print(f"Training finished at GEN {generation-1}!")
            save_ai_metadata(generation, best_score_display)
            return

        clock.tick(60)
        screen.blit(bg_img, (0, 0))

        # Spawn pipe
        if frame == 0 or frame % pipe_spawn_time == 0:
            gap_y = random.randint(120, 400)
            pipes.append({"x": WIDTH, "gap_y": gap_y, "passed": False, "scored": False})

        # Move pipes
        for p in pipes:
            p["x"] -= pipe_speed
            if not p["scored"] and p["x"] + pipe_width < 50:
                game_score += 1
                p["scored"] = True

        pipes = [p for p in pipes if p["x"] > -pipe_width]

        # Update birds
        alive_count = 0
        for b in birds:
            if not b.dead:
                b.update(pipes, gravity, jump_force, pipe_gap, HEIGHT, pipe_width)

                for p in pipes:
                    if not p["passed"] and b.x > p["x"] + pipe_width:
                        b.score += 1
                        p["passed"] = True
                        pipe_speed += 0.05

                b.draw(screen, bird_img)
                alive_count += 1

        # Draw pipes
        for p in pipes:
            screen.blit(pipe_top_img, (p["x"], p["gap_y"] - 500))
            screen.blit(pipe_img,     (p["x"], p["gap_y"] + pipe_gap))

        # HUD
        screen.blit(font.render(f"Generation: {generation}", True, (255, 255, 0)), (10, 10))
        screen.blit(font.render(f"Alive: {alive_count}", True, (0, 255, 0)), (10, 50))
        screen.blit(font.render(f"Best Score: {best_score_display}", True, (255, 150, 50)), (10, 90))
        screen.blit(font.render(f"Score: {game_score}", True, (255, 255, 255)), (10, 130))

        pygame.draw.rect(screen, (200, 30, 30), stop_rect)
        screen.blit(font.render("STOP", True, (255, 255, 255)), (stop_rect.x + 20, stop_rect.y + 5))

        pygame.display.update()

        # ============================
        #       ALL BIRDS DIE
        # ============================
        if alive_count == 0:
            best_bird = max(birds, key=lambda b: b.score)

            fitness_best = best_bird.score        # dùng cho log
            pipes_passed = game_score             # score đúng

            # ----- Update Best Score -----
            if pipes_passed > best_score_display:
                best_score_display = pipes_passed
                save_model(best_bird.brain)
                print("Saved new BEST model (based on Pipes Passed)!")

            # Save metadata
            save_ai_metadata(generation, best_score_display)

            # Log
            with open("ai_training_log.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"GEN {generation} | Pipes Passed = {pipes_passed} | Fitness Best = {fitness_best}\n"
                )

            # Prepare next generation
            birds = next_generation(birds, population)
            pipes = []
            frame = 0
            game_score = 0
            pipe_speed = 3
            generation += 1

            # spawn pipe
            gap_y = random.randint(120, 400)
            pipes.append({"x": WIDTH, "gap_y": gap_y, "passed": False, "scored": False})

        # STOP button
        mouse_pos = pygame.mouse.get_pos()
        if stop_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            print("Training stopped by user")
            save_ai_metadata(generation, best_score_display)
            return

        # ESC or Quit window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_ai_metadata(generation, best_score_display)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                save_ai_metadata(generation, best_score_display)
                return

        frame += 1

def highscore_screen():
    font_title = pygame.font.Font(None, 70)
    font_item = pygame.font.Font(None, 40)

    back_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 90, 160, 50)

    while True:
        screen.fill((20, 20, 30))
        mouse_pos = pygame.mouse.get_pos()

        # --- LOAD HIGHSCORES ---
        scores = load_highscore()
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # --- TITLE ---
        title = font_title.render("HIGH SCORES", True, (255, 255, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

        # --- SCORE LIST ---
        y = 130
        rank = 1
        for name, sc in sorted_scores[:10]:   # Hiển thị Top 10
            item = font_item.render(f"{rank}. {name} — {sc}", True, (255, 255, 255))
            screen.blit(item, (60, y))
            y += 45
            rank += 1

        # --- BACK BUTTON ---
        color = (50, 130, 220) if back_rect.collidepoint(mouse_pos) else (30, 90, 170)
        pygame.draw.rect(screen, color, back_rect, border_radius=10)

        back_text = font_item.render("Back", True, (255, 255, 255))
        screen.blit(back_text, (back_rect.centerx - back_text.get_width()//2,
                                back_rect.centery - back_text.get_height()//2))

        pygame.display.update()

        # --- EVENT ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(mouse_pos):
                    return

def game_over_menu(score, high_score, player_name):
    font_big = pygame.font.Font(None, 70)
    font_small = pygame.font.Font(None, 40)

    restart_rect = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 30, 240, 55)
    menu_rect    = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 110, 240, 55)
    quit_rect    = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 190, 240, 55)

    while True:
        screen.blit(gameover_bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # --- LẤY BEST SCORE TỪ FILE JSON ---
        scores = load_highscore()
        best_score = scores.get(player_name, 0)

        txt = font_big.render("GAME OVER", True, (255, 0, 0))
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 180))

        txt = font_small.render(f"Player: {player_name}", True, (255, 255, 255))
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 130))

        txt = font_small.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 80))

        txt = font_small.render(f"High Score: {best_score}", True, (255, 255, 0))
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 30))

        # Restart button
        color = (0, 200, 0) if restart_rect.collidepoint(mouse_pos) else (0, 150, 0)
        pygame.draw.rect(screen, color, restart_rect, border_radius=10)
        txt = font_small.render("Restart", True, (255, 255, 255))
        screen.blit(txt, (restart_rect.centerx - txt.get_width() // 2,
                          restart_rect.centery - txt.get_height() // 2))

        # Menu button
        color = (50, 130, 220) if menu_rect.collidepoint(mouse_pos) else (30, 90, 170)
        pygame.draw.rect(screen, color, menu_rect, border_radius=10)
        txt = font_small.render("Main Menu", True, (255, 255, 255))
        screen.blit(txt, (menu_rect.centerx - txt.get_width() // 2,
                          menu_rect.centery - txt.get_height() // 2))

        # Quit button
        color = (220, 50, 50) if quit_rect.collidepoint(mouse_pos) else (150, 20, 20)
        pygame.draw.rect(screen, color, quit_rect, border_radius=10)
        txt = font_small.render("Quit", True, (255, 255, 255))
        screen.blit(txt, (quit_rect.centerx - txt.get_width() // 2,
                          quit_rect.centery - txt.get_height() // 2))

        pygame.display.update()

        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_rect.collidepoint(mouse_pos):
                    return "restart"
                if menu_rect.collidepoint(mouse_pos):
                    return "menu"
                if quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    highscores = load_highscore()

    while True:
        mode, player_name = main_menu()

        if mode == "play":
            score = play_normal_game(player_name)

            highscores = load_highscore()
            old_score = highscores.get(player_name, 0)

            if score > old_score:
                highscores[player_name] = score
                save_highscore(highscores)

        elif mode == "scores":
            highscore_screen()

        elif mode == "train":
            train_ai()

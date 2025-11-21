import pygame
import random
import json
import os
import sys
from utils import send_score_to_server, asset_path, load_sound, in_browser

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

# ==========================
#   LOAD ASSETS
# ==========================
bg_img = pygame.image.load(asset_path('assets', 'background.png'))
bird_img = pygame.image.load(asset_path('assets', 'bird.png'))
pipe_img = pygame.image.load(asset_path('assets', 'pipe.png'))
menu_bg = pygame.image.load(asset_path('assets', 'menu_bg.png'))
gameover_bg = pygame.image.load(asset_path('assets', 'gameover_bg.png'))
play_btn = pygame.image.load(asset_path('assets', 'play_btn.png'))
play_btn_hover = pygame.image.load(asset_path('assets', 'play_btn_hover.png'))
train_btn = pygame.image.load(asset_path('assets', 'train_btn.png'))
train_btn_hover = pygame.image.load(asset_path('assets', 'train_btn_hover.png'))
quit_btn = pygame.image.load(asset_path('assets', 'quit_btn.png'))
quit_btn_hover = pygame.image.load(asset_path('assets', 'quit_btn_hover.png'))

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

# sounds will be loaded with helper (try .ogg then .wav)

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

clock = pygame.time.Clock()


# ================================================================
#   HÀM GỬI ĐIỂM LÊN SERVER FLASK
# ================================================================
flap_sound = load_sound('assets/flap') or load_sound('assets/flap.wav')
hit_sound = load_sound('assets/hit') or load_sound('assets/hit.wav')


# ================================================================
#   LOAD / SAVE SCORE LOCAL
# ================================================================
def load_highscore():
    if not os.path.exists(PLAYER_SCORE_FILE):
        save_highscore({})
        return {}

    try:
        with open(PLAYER_SCORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        save_highscore({})
        return {}

def save_highscore(data):
    with open(PLAYER_SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ================================================================
def draw_button_with_text(image, hover, rect, mouse_pos, text):
    font = pygame.font.Font(None, 40)
    txt = font.render(text, True, (255, 255, 255))
    txt_rect = txt.get_rect(center=rect.center)

    if rect.collidepoint(mouse_pos):
        screen.blit(hover, rect)
    else:
        screen.blit(image, rect)
    screen.blit(txt, txt_rect)


def main_menu(default_name=None):
    play_rect = pygame.Rect(WIDTH//2-100, HEIGHT//2-60, btn_width, btn_height)
    train_rect = pygame.Rect(WIDTH//2-100, HEIGHT//2+10, btn_width, btn_height)
    score_rect = pygame.Rect(WIDTH//2-100, HEIGHT//2+80, btn_width, btn_height)
    quit_rect = pygame.Rect(WIDTH//2-100, HEIGHT//2+160, btn_width, btn_height)

    font_title = pygame.font.Font(None, 80)

    while True:
        screen.blit(menu_bg, (0, 0))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        title = font_title.render("FLAPPY BIRD", True, (255,255,0))
        screen.blit(title, (WIDTH//2 - 200, HEIGHT//2 - 180))

        # Play
        draw_button_with_text(play_btn, play_btn_hover, play_rect, mouse, "Play")
        if play_rect.collidepoint(mouse) and click:
            if default_name:
                return ("play", default_name)
            else:
                return ("play", input_player_name())

        # Train
        draw_button_with_text(train_btn, train_btn_hover, train_rect, mouse, "Train AI")
        if train_rect.collidepoint(mouse) and click:
            return ("train", None)

        # Scores
        draw_button_with_text(play_btn, play_btn_hover, score_rect, mouse, "Scores")
        if score_rect.collidepoint(mouse) and click:
            return ("scores", None)

        # Quit
        draw_button_with_text(quit_btn, quit_btn_hover, quit_rect, mouse, "Quit")
        if quit_rect.collidepoint(mouse) and click:
            pygame.quit()
            sys.exit()

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def input_player_name():
    font = pygame.font.Font(None, 50)
    name = ""

    while True:
        screen.fill((20,20,30))
        text = font.render("Enter Your Name:", True, (255,255,0))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 200))

        box = pygame.Rect(WIDTH//2 -150, 260, 300, 60)
        pygame.draw.rect(screen, (100,100,100), box)

        name_surf = font.render(name, True, (255,255,255))
        screen.blit(name_surf, (box.x+10, box.y+10))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    if len(name.strip()) > 0:
                        return name
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12:
                        name += e.unicode


# ================================================================
#   AI TRAINING
# ================================================================
async def train_ai():
    print("Starting AI Training...")
    # Placeholder: In a real implementation, this would run the genetic algorithm loop
    # similar to play_normal_game but with multiple birds and no rendering (or fast rendering).
    import asyncio
    while True:
        await asyncio.sleep(1)
        print("AI is training... (Press Stop to exit)")

# ================================================================
#   GAME LOOP
# ================================================================
def play_normal_game(player_name):
    global highscores

    bird = pygame.Rect(50, 300, 40, 30)
    bird_speed = 0
    pipe_x = WIDTH
    pipe_height = random.randint(100, 350)
    pipe_speed = 3
    score = 0
    paused = False

    while True:
        clock.tick(60)

        # events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    paused = not paused
                if e.key == pygame.K_SPACE:
                    bird_speed = jump_force
                    flap_sound.play()

        if paused:
            continue

        # update bird
        bird_speed += gravity
        bird.y += int(bird_speed)

        # pipes
        pipe_x -= pipe_speed
        if pipe_x < -pipe_width:
            pipe_x = WIDTH
            pipe_height = random.randint(100, 350)
            score += 1

        pipe_top = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
        pipe_bottom = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT)

        # collision
        if bird.colliderect(pipe_top) or bird.colliderect(pipe_bottom) or bird.y < 0 or bird.y > HEIGHT:

            hit_sound.play()

            scores = load_highscore()
            best = scores.get(player_name, 0)

            if score > best:
                scores[player_name] = score
                save_highscore(scores)

            # 🔥 Gửi điểm lên web
            send_score_to_server(player_name, score)

            return score

        # draw
        screen.blit(bg_img, (0,0))
        screen.blit(bird_img, bird)
        screen.blit(pipe_top_img, (pipe_x, pipe_height - 500))
        screen.blit(pipe_img, (pipe_x, pipe_height + pipe_gap))

        font = pygame.font.Font(None, 40)
        screen.blit(font.render(f"Player: {player_name}", True, (255,255,255)), (10,10))
        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,50))

        pygame.display.update()


# ================================================================
#   MAIN
# ================================================================
if __name__ == "__main__":
    highscores = load_highscore()

    # Flask sẽ gọi:
    #     python flappy.py username
    default_name = sys.argv[1] if len(sys.argv) > 1 else None

    while True:
        mode, player_name = main_menu(default_name)

        if mode == "play":
            play_normal_game(player_name)

        elif mode == "scores":
            pass

        elif mode == "train":
            import asyncio
            asyncio.run(train_ai())

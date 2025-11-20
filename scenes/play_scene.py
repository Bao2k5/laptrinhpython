import pygame
import sys
import random
from database import save_score

WIDTH, HEIGHT = 500, 600


class PlayScene:
    def __init__(self, screen, player_name):
        self.screen = screen
        self.player_name = player_name

        # Background
        self.bg = pygame.image.load(asset_path('assets', 'background.png')).convert()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

        # Bird
        self.bird_img = pygame.image.load(asset_path('assets', 'bird.png')).convert_alpha()
        self.bird_img = pygame.transform.scale(self.bird_img, (40, 30))

        # Pipes
        self.pipe_img = pygame.image.load(asset_path('assets', 'pipe.png')).convert_alpha()
        self.pipe_img = pygame.transform.scale(self.pipe_img, (80, 500))
        self.pipe_top_img = pygame.transform.flip(self.pipe_img, False, True)

        # Sounds
        self.flap_sound = load_sound('assets/flap') or load_sound('assets/flap.wav')
        self.hit_sound = load_sound('assets/hit') or load_sound('assets/hit.wav')

        self.font = pygame.font.Font(None, 40)

    def run(self):
        # Bird physics
        bird = pygame.Rect(80, 250, 40, 30)
        bird_vel = 0
        gravity = 0.4
        jump_force = -7

        # Pipes
        pipe_width = 80
        pipe_gap = 150
        pipe_x = WIDTH
        pipe_h = random.randint(100, 350)
        pipe_speed = 3

        # Score
        score = 0
        level = 1
        score_to_level = 10

        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            # -------- EVENT --------
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        bird_vel = jump_force
                        self.flap_sound.play()

                    if e.key == pygame.K_ESCAPE:
                        return "menu", {"player": self.player_name}

            # -------- UPDATE --------
            bird_vel += gravity
            bird.y += int(bird_vel)

            pipe_x -= pipe_speed

            # Pipe passed -> +1 score (CHỈ MỘT LẦN)
            if pipe_x < -pipe_width:
                pipe_x = WIDTH
                pipe_h = random.randint(100, 350)
                score += 1                     # <<< CHỈ TĂNG TẠI ĐÂY
                if score % score_to_level == 0:
                    level += 1
                    pipe_speed += 0.7

            pipe_top = pygame.Rect(pipe_x, 0, pipe_width, pipe_h)
            pipe_bottom = pygame.Rect(pipe_x, pipe_h + pipe_gap, pipe_width, HEIGHT)

            # -------- COLLISION --------
            if (bird.colliderect(pipe_top) or
                bird.colliderect(pipe_bottom) or
                bird.y < 0 or bird.y > HEIGHT):

                self.hit_sound.play()

                # Lưu điểm vào Mongo
                save_score(self.player_name, score)

                return "gameover", {
                    "player": self.player_name,
                    "score": score
                }

            # -------- DRAW --------
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.pipe_top_img, (pipe_x, pipe_h - 500))
            self.screen.blit(self.pipe_img, (pipe_x, pipe_h + pipe_gap))
            self.screen.blit(self.bird_img, bird)

            score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

            lvl_text = self.font.render(f"Level: {level}", True, (255, 255, 0))
            self.screen.blit(lvl_text, (10, 50))

            player_text = self.font.render(f"Player: {self.player_name}", True, (255, 255, 255))
            self.screen.blit(player_text, (260, 10))

            pygame.display.update()

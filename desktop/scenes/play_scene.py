import pygame
import sys
import random
import asyncio
from game_utils import asset_path, load_sound

WIDTH, HEIGHT = 500, 600

class Coin:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load(asset_path('assets', 'coin.png')), (30, 30))
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def move(self, speed):
        self.rect.x -= speed
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class PlayScene:
    def __init__(self, screen, player_name, api=None, storage=None):
        self.screen = screen
        self.player_name = player_name
        self.api = api
        self.storage = storage

        # --- LOAD SETTINGS ---
        self.current_skin = self.storage.get_current_skin() if self.storage else "yellow"
        
        # --- ASSETS SETUP ---
        # 1. Random Background
        bg_file = random.choice(['background-day.png', 'background-night.png'])
        self.bg = pygame.image.load(asset_path('assets', bg_file)).convert()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

        # 2. Random Pipe Color
        pipe_file = random.choice(['pipe-green.png', 'pipe-red.png'])
        self.pipe_img = pygame.image.load(asset_path('assets', pipe_file)).convert_alpha()
        self.pipe_img = pygame.transform.scale(self.pipe_img, (80, 500))
        self.pipe_top_img = pygame.transform.flip(self.pipe_img, False, True)

        # 3. Base (Ground)
        self.base_img = pygame.image.load(asset_path('assets', 'base.png')).convert()
        self.base_img = pygame.transform.scale(self.base_img, (WIDTH, 100))
        self.base_x = 0

        # 4. Bird Animation Frames (Based on Skin)
        skin_map = {
            "yellow": ["bird-up.png", "bird-mid.png", "bird-down.png"],
            "blue": ["bluebird-upflap.png", "bluebird-midflap.png", "bluebird-downflap.png"],
            "red": ["redbird-upflap.png", "redbird-midflap.png", "redbird-downflap.png"]
        }
        files = skin_map.get(self.current_skin, skin_map["yellow"])
        
        self.bird_frames = [
            pygame.transform.scale(pygame.image.load(asset_path('assets', f)).convert_alpha(), (40, 30))
            for f in files
        ]
        self.bird_index = 0
        self.bird_img = self.bird_frames[self.bird_index]
        self.anim_counter = 0

        # Sounds
        self.flap_sound = load_sound('assets/flap.wav')
        self.hit_sound = load_sound('assets/hit.wav')
        self.point_sound = load_sound('assets/flap.wav')  # Use flap sound as fallback
        self.coin_sound = load_sound('assets/flap.wav')  # Use flap sound for coin

        self.font = pygame.font.Font(None, 40)
        self.coin_icon = pygame.transform.scale(pygame.image.load(asset_path('assets', 'coin.png')), (25, 25))

    async def run(self):
        # --- ABILITIES CONFIG ---
        gravity = 0.4
        jump_force = -7
        score_multiplier = 1
        
        if self.current_skin == "blue":
            gravity = 0.3  # Floaty
            jump_force = -6
        elif self.current_skin == "red":
            gravity = 0.5  # Heavy
            score_multiplier = 2 # Double Score

        # Bird physics
        bird = pygame.Rect(80, 250, 40, 30)
        bird_vel = 0

        # Pipes
        pipe_width = 80
        pipe_gap = 160
        pipe_x = WIDTH
        pipe_h = random.randint(100, 300)
        pipe_speed = 3

        # Score & Coins
        score = 0
        coins_collected = 0
        level = 1
        score_to_level = 10

        powerups = []
        coins_list = [] # List of Coin objects
        shield_timer = 0

        clock = pygame.time.Clock()
        game_active = True

        while True:
            await asyncio.sleep(0)
            clock.tick(60)

            # -------- EVENT --------
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE and game_active:
                        bird_vel = jump_force
                        if self.flap_sound:
                            self.flap_sound.play()

                    if e.key == pygame.K_ESCAPE:
                        return "menu", {"player": self.player_name}

            # -------- UPDATE --------
            if game_active:
                # 1. Bird Movement
                bird_vel += gravity
                bird.y += int(bird_vel)

                # 2. Bird Animation
                self.anim_counter += 1
                if self.anim_counter >= 5:
                    self.bird_index = (self.bird_index + 1) % 3
                    self.bird_img = self.bird_frames[self.bird_index]
                    self.anim_counter = 0
                
                rotated_bird = pygame.transform.rotate(self.bird_img, -bird_vel * 3)

                # 3. Base Movement
                self.base_x -= pipe_speed
                if self.base_x <= -WIDTH:
                    self.base_x = 0

                # 4. Pipe Movement
                pipe_x -= pipe_speed

                # Pipe passed -> Score
                if pipe_x < -pipe_width:
                    pipe_x = WIDTH
                    pipe_h = random.randint(100, 300)
                    score += 1 * score_multiplier # Apply multiplier
                    
                    if self.point_sound:
                        self.point_sound.play()
                        
                    if score % score_to_level == 0:
                        level += 1
                        pipe_speed += 0.5

                pipe_top = pygame.Rect(pipe_x, 0, pipe_width, pipe_h)
                pipe_bottom = pygame.Rect(pipe_x, pipe_h + pipe_gap, pipe_width, HEIGHT - 100)

                # 5. Spawn Coins (30% chance when pipe resets)
                if pipe_x == WIDTH and random.random() < 0.5:
                    # Spawn coin in the gap
                    cy = pipe_h + pipe_gap // 2 - 15
                    coins_list.append(Coin(WIDTH + 40, cy))

                # 6. Move & Check Coins
                for c in coins_list[:]:
                    c.move(pipe_speed)
                    if c.rect.right < 0:
                        coins_list.remove(c)
                    elif bird.colliderect(c.rect):
                        coins_collected += 1
                        if self.storage:
                            self.storage.add_coins(1)
                        if self.coin_sound:
                            self.coin_sound.play()
                        coins_list.remove(c)

                # 7. Powerups Logic (Existing)
                if random.randint(0, 400) == 0:
                    p_type = random.choice(['shield']) # Magnet logic needs update for coins, keep shield for now
                    powerups.append(PowerUp(WIDTH, random.randint(50, 400), p_type))

                for p in powerups[:]:
                    p.move(pipe_speed)
                    if p.rect.right < 0:
                        powerups.remove(p)
                    elif bird.colliderect(p.rect):
                        if p.type == 'shield':
                            shield_timer = 300
                        powerups.remove(p)

                # -------- COLLISION --------
                if (bird.colliderect(pipe_top) or 
                    bird.colliderect(pipe_bottom) or 
                    bird.y < 0 or 
                    bird.y > HEIGHT - 100 - bird.height):

                    if shield_timer > 0:
                        pass
                    else:
                        if self.hit_sound:
                            self.hit_sound.play()
                        
                        # Game Over
                        print(f"Game Over! Score: {score}")
                        saved = False
                        if self.api:
                            saved = self.api.save_score(self.player_name, score)
                        if not saved and self.storage:
                            self.storage.save_pending_score(self.player_name, score)

                        return "gameover", {
                            "player": self.player_name,
                            "score": score
                        }

            # -------- DRAW --------
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.pipe_top_img, (pipe_x, pipe_h - 500))
            self.screen.blit(self.pipe_img, (pipe_x, pipe_h + pipe_gap))
            
            # Draw Coins
            for c in coins_list:
                c.draw(self.screen)
                
            # Draw Powerups
            for p in powerups:
                p.draw(self.screen)

            self.screen.blit(self.base_img, (self.base_x, HEIGHT - 100))
            self.screen.blit(self.base_img, (self.base_x + WIDTH, HEIGHT - 100))

            if game_active:
                new_rect = rotated_bird.get_rect(center=bird.center)
                self.screen.blit(rotated_bird, new_rect.topleft)
            else:
                self.screen.blit(self.bird_img, bird)

            if shield_timer > 0:
                pygame.draw.circle(self.screen, (0, 255, 255), bird.center, 35, 3)
                shield_timer -= 1

            # UI
            score_text = self.font.render(f"{score}", True, (255, 255, 255))
            score_shadow = self.font.render(f"{score}", True, (0, 0, 0))
            self.screen.blit(score_shadow, (WIDTH//2 + 2, 52))
            self.screen.blit(score_text, (WIDTH//2, 50))
            
            # Coin UI
            self.screen.blit(self.coin_icon, (10, 10))
            coin_txt = self.font.render(f"{coins_collected}", True, (255, 215, 0))
            self.screen.blit(coin_txt, (40, 10))

            pygame.display.update()


class PowerUp:
    def __init__(self, x, y, type_name):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.type = type_name # 'shield', 'magnet'
        self.img = pygame.image.load(asset_path('assets', f'{type_name}.png')).convert_alpha()
        self.img = pygame.transform.scale(self.img, (30, 30))

    def move(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        screen.blit(self.img, self.rect)

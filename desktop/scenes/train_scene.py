import pygame
import sys
import os
import asyncio
import random
import numpy as np
from pathlib import Path
from game_utils import asset_path

# Add parent directory to path to import BirdAI
import sys
import os

# Get the root directory of the project
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from AI.bird_ai import BirdAI
    print("Successfully imported BirdAI from:", os.path.join(root_dir, 'AI', 'bird_ai.py'))
except ImportError as e:
    print(f"Error importing BirdAI: {e}")
    print("Current sys.path:", sys.path)
    print("Files in AI directory:", os.listdir(os.path.join(root_dir, 'AI')))
    raise

# Game constants
WIDTH = 500
HEIGHT = 600
GRAVITY = 0.25
JUMP_FORCE = -7
# Làm game train dễ hơn một chút
PIPE_GAP = 200          # khe hở ống rộng hơn
PIPE_FREQUENCY = 2000   # thời gian giữa 2 ống xa hơn (ms)

class TrainScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 30)
        self.running = True
        
        self.bg = pygame.image.load(asset_path('assets', 'background-day.png')).convert()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

        pipe_image = pygame.image.load(asset_path('assets', 'pipe-green.png')).convert_alpha()
        self.pipe_img = pygame.transform.scale(pipe_image, (80, 500))
        self.pipe_top_img = pygame.transform.flip(self.pipe_img, False, True)

        self.base_img = pygame.image.load(asset_path('assets', 'base.png')).convert()
        self.base_img = pygame.transform.scale(self.base_img, (WIDTH, 100))
        
    def draw_text(self, text, y, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        screen_width = self.screen.get_width()
        text_rect = text_surface.get_rect(center=(screen_width//2, y))
        self.screen.blit(text_surface, text_rect)
    
    def create_pipe(self):
        return {
            # Cho ống xuất hiện xa chim hơn một chút để có thời gian phản ứng
            "x": WIDTH + 120,
            "gap_y": random.randint(150, HEIGHT - 250),
            "gap": PIPE_GAP,
            "scored": False
        }
        
    async def run_generation(self, birds, pipes, base_x, last_pipe):
        clock = pygame.time.Clock()
        alive_birds = [bird for bird in birds if not bird.dead]
        
        while alive_birds:
            current_time = pygame.time.get_ticks()
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False, None, None, None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False, None, None, None
            
            # Update pipes
            if current_time - last_pipe > PIPE_FREQUENCY:
                pipes.append(self.create_pipe())
                last_pipe = current_time

            # Move pipes to the left so they appear and scroll
            for p in pipes:
                p["x"] -= 3
            
            # Update game state (ground movement)
            base_x -= 3
            if base_x <= -WIDTH:
                base_x = 0
            
            # Update birds
            for bird in alive_birds[:]:
                if bird.dead:
                    alive_birds.remove(bird)
                    continue
                    
                # Find the closest pipe in front of the bird
                next_pipe = None
                for pipe in pipes:
                    if pipe["x"] + 80 > bird.x:
                        next_pipe = pipe
                        break

                # Let the bird's neural network decide whether to jump
                if next_pipe:
                    should_jump = bird.think(
                        [next_pipe],
                        HEIGHT,
                        pipe_width=80
                    )
                    if should_jump:
                        bird.speed = JUMP_FORCE
                
                # Update bird physics
                bird.speed += GRAVITY
                bird.y += bird.speed
                bird.score += 1
                
                # Check for collisions with ground/ceiling
                if bird.y < 0 or bird.y > HEIGHT - 100:
                    bird.dead = True
                    bird.fitness = bird.score - abs(bird.y - (HEIGHT/2)) * 0.1
                    continue
                
                # Check pipe collisions and scoring
                if next_pipe:
                    if (bird.x + 40 > next_pipe["x"] and 
                        bird.x < next_pipe["x"] + 80):
                        if (bird.y < next_pipe["gap_y"] or 
                            bird.y + 30 > next_pipe["gap_y"] + PIPE_GAP):
                            bird.dead = True
                            bird.fitness = bird.score - abs(bird.y - (next_pipe["gap_y"] + PIPE_GAP/2)) * 0.1
                            continue
                    
                    # Score point when passing the pipe
                    if not next_pipe.get("scored", False) and bird.x > next_pipe["x"] + 80:
                        next_pipe["scored"] = True
                        bird.score += 1
            
            # Remove off-screen pipes
            pipes = [p for p in pipes if p["x"] > -80]
            
            # Draw everything
            self.screen.blit(self.bg, (0, 0))
            
            # Draw pipes
            for p in pipes:
                # Draw top pipe
                self.screen.blit(self.pipe_top_img, (p["x"], p["gap_y"] - 500))
                # Draw bottom pipe
                self.screen.blit(self.pipe_img, (p["x"], p["gap_y"] + PIPE_GAP))
            
            # Draw base
            self.screen.blit(self.base_img, (base_x, HEIGHT - 100))
            self.screen.blit(self.base_img, (base_x + WIDTH, HEIGHT - 100))
            
            # Draw birds
            for bird in alive_birds:
                bird.draw(self.screen, self.bird_img)
            
            # Draw UI
            gen_text = self.font.render(f"Gen: {self.generation}", True, (0, 0, 0))
            alive_text = self.font.render(f"Alive: {len(alive_birds)}", True, (0, 0, 0))
            score_text = self.font.render(f"Score: {max([b.score for b in birds] if birds else [0])}", True, (0, 0, 0))
            
            self.screen.blit(gen_text, (10, 10))
            self.screen.blit(alive_text, (10, 50))
            self.screen.blit(score_text, (10, 90))
            
            pygame.display.flip()
            clock.tick(60)
            
        return True, pipes, base_x, last_pipe
    
    def next_generation(self, birds):
        # Calculate fitness
        for bird in birds:
            bird.fitness = bird.score ** 2
        
        # Sort by fitness
        birds.sort(key=lambda x: x.fitness, reverse=True)
        
        # Keep top 20%
        keep = int(len(birds) * 0.2)
        new_birds = birds[:keep]
        
        # Repopulate with crossover and mutation
        while len(new_birds) < len(birds):
            parent1 = random.choice(birds[:keep])
            parent2 = random.choice(birds[:keep])
            
            # Create new bird with crossover
            child = parent1.clone()
            child.brain = parent1.brain.crossover(parent2.brain)
            child.brain.mutate(0.1)
            new_birds.append(child)
        
        # Save best model
        if new_birds:
            new_birds[0].save_best()
        
        return new_birds
    
    async def run(self):
        # Use existing screen from DesktopGame, only (re)create font if needed
        self.font = pygame.font.SysFont('Arial', 30)
        
        # Load bird image (simple colored rectangle)
        self.bird_img = pygame.Surface((40, 30))
        self.bird_img.fill((255, 255, 0))  # Yellow bird
        bird_sprite = pygame.transform.scale(
            pygame.image.load(asset_path('assets', 'bird-mid.png')).convert_alpha(),
            (40, 30)
        )
        self.bird_img = bird_sprite
        
        # Initialize population
        population_size = 50
        self.generation = 0
        birds = [BirdAI() for _ in range(population_size)]
        
        # Game state
        pipes = [self.create_pipe()]
        base_x = 0
        last_pipe = pygame.time.get_ticks()
        
        try:
            while True:
                # Run generation
                self.generation += 1
                
                # Show generation info
                self.screen.fill((10, 10, 20))
                screen_height = self.screen.get_height()
                self.draw_text(f"Thế hệ: {self.generation}", screen_height//2 - 50, (255, 255, 255))
                self.draw_text(f"Số chim: {len(birds)}", screen_height//2, (255, 255, 255))
                pygame.display.flip()
                
                # Run the generation
                continue_training, pipes, base_x, last_pipe = await self.run_generation(
                    birds, pipes, base_x, last_pipe
                )
                
                if not continue_training:
                    break
                    
                # Create next generation
                birds = self.next_generation(birds)
                
                # Reset game state
                pipes = [self.create_pipe()]
                base_x = 0
                last_pipe = pygame.time.get_ticks()
                
                # Reset birds
                for bird in birds:
                    bird.__init__(brain=bird.brain)
                    
        except Exception as e:
            print(f"Lỗi khi train AI: {str(e)}")
            import traceback
            traceback.print_exc()
        
        return "menu", {"player": None}

import pygame
import sys
import os
import random

# Add parent directory to path to import AI module
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from AI.bird_ai import BirdAI
from game_utils import asset_path, load_sound

WIDTH, HEIGHT = 500, 600

def train_ai():
    """
    Run the AI training loop
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)

    # --- ASSETS ---
    bg_img = pygame.image.load(asset_path('assets', 'background-day.png')).convert()
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
    
    pipe_img = pygame.image.load(asset_path('assets', 'pipe-green.png')).convert_alpha()
    pipe_img = pygame.transform.scale(pipe_img, (80, 500))
    pipe_top_img = pygame.transform.flip(pipe_img, False, True)
    
    base_img = pygame.image.load(asset_path('assets', 'base.png')).convert()
    base_img = pygame.transform.scale(base_img, (WIDTH, 100))
    
    bird_img = pygame.transform.scale(pygame.image.load(asset_path('assets', 'bird-mid.png')).convert_alpha(), (40, 30))

    # --- VARIABLES ---
    generation = 1
    birds = [BirdAI() for _ in range(50)]
    
    pipes = []
    pipe_width = 80
    pipe_gap = 150
    pipe_frequency = 1500 # ms
    last_pipe = pygame.time.get_ticks()
    
    base_x = 0
    speed = 3
    
    run = True
    while run:
        clock.tick(60)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        # Spawn Pipes
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > pipe_frequency:
            pipe_h = random.randint(100, 350)
            pipes.append({
                "x": WIDTH,
                "gap_y": pipe_h, # Top of the bottom pipe (gap starts here? No, wait)
                # In bird_ai.py: dy_top = (nearest["gap_y"] - self.y)
                # dy_bottom = (nearest["gap_y"] + gap - self.y)
                # So gap_y should be the y-coordinate of the top of the gap?
                # Let's check update logic in bird_ai.py
                # dy_top = (nearest["gap_y"] - self.y) / height
                # If gap_y is the top edge of the gap (bottom of top pipe), then dy_top is distance to it.
                # Let's assume gap_y is the Y position where the gap starts (bottom of top pipe).
            })
            last_pipe = current_time

        # Update Pipes
        for p in pipes:
            p["x"] -= speed
        
        if pipes and pipes[0]["x"] < -pipe_width:
            pipes.pop(0)

        # Update Base
        base_x -= speed
        if base_x <= -WIDTH:
            base_x = 0

        # Update Birds
        alive_birds = [b for b in birds if not b.dead]
        
        if len(alive_birds) == 0:
            # Next Generation
            generation += 1
            pipes = []
            last_pipe = pygame.time.get_ticks()
            
            # Genetic Algorithm: Select best and mutate
            birds.sort(key=lambda x: x.score, reverse=True)
            best_bird = birds[0]
            
            # Save best model occasionally
            if best_bird.score > 50: # Only save if decent
                best_bird.brain.save("ai_best_model.npz")
            
            new_birds = []
            # Keep top 5 as is (Elitism)
            for i in range(5):
                new_birds.append(BirdAI(brain=birds[i].brain))
            
            # Fill rest with mutated clones of top 10
            for _ in range(45):
                parent = random.choice(birds[:10])
                new_birds.append(BirdAI(brain=parent.brain))
            
            birds = new_birds
            continue

        # Update logic for each bird
        # We need to pass the nearest pipe to the bird
        # Find nearest pipe in front of bird
        
        # Filter pipes that are to the right of the bird (or overlapping)
        # Bird x is 50. Pipe width 80.
        # We want the first pipe where p["x"] + pipe_width > bird.x
        
        # bird_ai.py logic:
        # for p in pipes:
        #    if p["x"] + pipe_width >= self.x:
        #        nearest = p
        #        break
        
        # So we just pass the whole list of pipes, bird_ai handles finding nearest.
        # But wait, bird_ai expects pipes to be a list of dicts with "x" and "gap_y".
        
        for bird in alive_birds:
            bird.update(pipes, 0.5, -8, pipe_gap, HEIGHT, pipe_width)

        # Draw
        screen.blit(bg_img, (0, 0))
        
        for p in pipes:
            # Draw top pipe
            # gap_y is the bottom of the top pipe
            # pipe_top_img height is 500.
            # We want the bottom of pipe_top_img to be at p["gap_y"]
            screen.blit(pipe_top_img, (p["x"], p["gap_y"] - 500))
            
            # Draw bottom pipe
            # Top of bottom pipe is gap_y + gap
            screen.blit(pipe_img, (p["x"], p["gap_y"] + pipe_gap))
            
        screen.blit(base_img, (base_x, HEIGHT - 100))
        
        for bird in alive_birds:
            bird.draw(screen, bird_img)
            
        # UI
        gen_txt = font.render(f"Gen: {generation}", True, (255, 255, 255))
        alive_txt = font.render(f"Alive: {len(alive_birds)}", True, (255, 255, 255))
        score_txt = font.render(f"Best: {max([b.score for b in birds])}", True, (255, 255, 255))
        
        screen.blit(gen_txt, (10, 10))
        screen.blit(alive_txt, (10, 50))
        screen.blit(score_txt, (10, 90))
        
        pygame.display.update()
    
    # Cleanup when exiting loop
    # Don't quit pygame here if we want to return to menu, just return
    return

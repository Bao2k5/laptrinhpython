import os
import sys
import pygame
import random
import numpy as np
from pathlib import Path

# Add the parent directory to path so we can import AI
sys.path.append(str(Path(__file__).parent.parent))
from AI.bird_ai import BirdAI

# Game constants
WIDTH = 500
HEIGHT = 600
GRAVITY = 0.25
JUMP_FORCE = -7
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

class AITrainer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird AI Training")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 30)
        
        # Load images
        self.bird_img = pygame.Surface((40, 30))
        self.bird_img.fill((255, 255, 0))  # Yellow bird
        
        self.pipe_img = pygame.Surface((80, 400))
        self.pipe_img.fill((0, 200, 0))  # Green pipes
        
        # Training parameters
        self.population_size = 50
        self.generation = 0
        self.high_score = 0
        
        # Initialize population
        self.population = [BirdAI() for _ in range(self.population_size)]
        
    def reset_game(self):
        self.pipes = [{"x": WIDTH, "gap_y": random.randint(150, HEIGHT - 250)}]
        self.base_x = 0
        self.score = 0
        self.last_pipe = pygame.time.get_ticks()
        
    def create_pipe(self):
        return {
            "x": WIDTH,
            "gap_y": random.randint(150, HEIGHT - 250),
            "scored": False
        }
        
    def run_generation(self):
        self.reset_game()
        alive_birds = [bird for bird in self.population]
        
        running = True
        while running and alive_birds:
            current_time = pygame.time.get_ticks()
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            
            # Update pipes
            if current_time - self.last_pipe > PIPE_FREQUENCY:
                self.pipes.append(self.create_pipe())
                self.last_pipe = current_time
            
            # Update game state
            self.base_x = (self.base_x - 2) % 100
            
            # Update birds
            for bird in alive_birds[:]:
                if bird.dead:
                    alive_birds.remove(bird)
                    continue
                    
                # Get closest pipe
                next_pipe = None
                for pipe in self.pipes:
                    if pipe["x"] + 80 > bird.x:
                        next_pipe = pipe
                        break
                
                # Bird thinking
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
                
                # Check for collisions
                if bird.y < 0 or bird.y > HEIGHT - 100:
                    bird.dead = True
                    bird.fitness = bird.score - abs(bird.y - (HEIGHT/2)) * 0.1
                    continue
                
                # Check pipe collisions
                if next_pipe:
                    if (bird.x + 40 > next_pipe["x"] and 
                        bird.x < next_pipe["x"] + 80):
                        if (bird.y < next_pipe["gap_y"] or 
                            bird.y + 30 > next_pipe["gap_y"] + PIPE_GAP):
                            bird.dead = True
                            bird.fitness = bird.score - abs(bird.y - (next_pipe["gap_y"] + PIPE_GAP/2)) * 0.1
                            continue
                    
                    # Score point
                    if not next_pipe.get("scored", False) and bird.x > next_pipe["x"] + 80:
                        next_pipe["scored"] = True
                        bird.score += 1
                        self.high_score = max(self.high_score, bird.score)
            
            # Remove off-screen pipes
            self.pipes = [p for p in self.pipes if p["x"] > -80]
            
            # Draw everything
            self.screen.fill((135, 206, 235))  # Sky blue background
            
            # Draw pipes
            for p in self.pipes:
                # Draw top pipe (flipped)
                pygame.draw.rect(self.screen, (0, 200, 0), 
                               (p["x"], 0, 80, p["gap_y"]))
                # Draw bottom pipe
                pygame.draw.rect(self.screen, (0, 200, 0),
                               (p["x"], p["gap_y"] + PIPE_GAP, 80, HEIGHT - p["gap_y"] - PIPE_GAP))
            
            # Draw base
            pygame.draw.rect(self.screen, (139, 69, 19), (0, HEIGHT - 100, WIDTH, 100))
            pygame.draw.rect(self.screen, (0, 200, 0), (self.base_x, HEIGHT - 100, WIDTH, 20))
            
            # Draw birds
            for bird in alive_birds:
                bird.draw(self.screen, self.bird_img)
            
            # Draw UI
            gen_text = self.font.render(f"Gen: {self.generation}", True, (0, 0, 0))
            alive_text = self.font.render(f"Alive: {len(alive_birds)}", True, (0, 0, 0))
            score_text = self.font.render(f"Score: {max([b.score for b in self.population] if self.population else [0])}", True, (0, 0, 0))
            high_score_text = self.font.render(f"High: {self.high_score}", True, (0, 0, 0))
            
            self.screen.blit(gen_text, (10, 10))
            self.screen.blit(alive_text, (10, 50))
            self.screen.blit(score_text, (10, 90))
            self.screen.blit(high_score_text, (10, 130))
            
            pygame.display.flip()
            self.clock.tick(60)
            
        return True
    
    def next_generation(self):
        # Calculate fitness
        for bird in self.population:
            bird.fitness = bird.score ** 2
        
        # Sort by fitness
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        
        # Keep top 20%
        keep = int(self.population_size * 0.2)
        new_population = self.population[:keep]
        
        # Repopulate with crossover and mutation
        while len(new_population) < self.population_size:
            parent1 = random.choice(self.population[:keep])
            parent2 = random.choice(self.population[:keep])
            
            # Crossover
            child = parent1.brain.crossover(parent2.brain)
            
            # Mutation
            child.mutate(0.1)
            
            # Create new bird with this brain
            new_bird = BirdAI(brain=child)
            new_population.append(new_bird)
        
        self.population = new_population
        self.generation += 1
        
        # Save best model
        if self.population:
            self.population[0].save_best()
    
    def run(self):
        try:
            while True:
                if not self.run_generation():
                    break
                self.next_generation()
        except KeyboardInterrupt:
            print("\nTraining stopped by user")
        finally:
            pygame.quit()

if __name__ == "__main__":
    trainer = AITrainer()
    trainer.run()

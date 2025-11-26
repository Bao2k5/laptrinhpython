import numpy as np
import random
import os
import pygame
from .neural_network import NeuralNetwork

BIRD_W = 40
BIRD_H = 30

class BirdAI:
    def __init__(self, brain=None, load_best=False):
        self.x = 50
        self.y = 300
        self.speed = 0
        self.dead = False
        self.score = 0
        self.fitness = 0
        self.genome = []
        self.brain = None
        
        if load_best:
            self.brain = NeuralNetwork()
            if not self.brain.load("ai_best_model.npz"):
                self.brain = NeuralNetwork()
                print("Using new random brain")
        elif brain is not None:
            self.brain = brain.clone()
            # Slight mutation for diversity
            self.brain.mutate(0.1)
        else:
            self.brain = NeuralNetwork()

    def think(self, pipes, height, pipe_width=80):
        if self.dead or len(pipes) == 0:
            return False

        # Find the next pipe
        next_pipe = None
        for pipe in pipes:
            if pipe["x"] + pipe_width > self.x:
                next_pipe = pipe
                break

        if next_pipe is None:
            return False

        # Normalized inputs
        dx = (next_pipe["x"] - self.x) / 500.0
        dy_top = (next_pipe["gap_y"] - self.y) / height
        dy_bottom = (next_pipe["gap_y"] + next_pipe["gap"] - self.y) / height
        current_speed = self.speed / 20.0  # Normalize speed

        # Create input array
        inputs = np.array([
            dx,
            dy_top,
            dy_bottom,
            current_speed,
            self.y / height
        ])

        # Get decision from neural network
        output = self.brain.forward(inputs)
        return output > 0.5

    def update(self, pipes, gravity, jump_force, gap, height, pipe_width=80):
        if self.dead:
            return

        # Physics update
        self.speed += gravity
        self.y += self.speed
        self.score += 1

        # Check if should jump
        if self.think(pipes, height, pipe_width):
            self.speed = jump_force

        # Check for collisions with top/bottom
        if self.y < 0 or self.y + BIRD_H > height:
            self.dead = True
            self.fitness = self.score - abs(self.y - height/2) * 0.1
            return

        # Check for collisions with pipes
        for pipe in pipes:
            if (self.x + BIRD_W > pipe["x"] and 
                self.x < pipe["x"] + pipe_width):
                if (self.y < pipe["gap_y"] or 
                    self.y + BIRD_H > pipe["gap_y"] + gap):
                    self.dead = True
                    self.fitness = self.score - abs(self.y - (pipe["gap_y"] + gap/2)) * 0.1
                    return

    def calculate_fitness(self):
        self.fitness = self.score ** 2
        return self.fitness

    def clone(self):
        clone = BirdAI(brain=self.brain)
        clone.fitness = self.fitness
        clone.score = self.score
        return clone

    def save_best(self):
        """Save the best model"""
        self.brain.save("ai_best_model.npz")

    def draw(self, screen, bird_img):
        if not self.dead:
            try:
                # Get bird rectangle for proper rotation
                bird_rect = bird_img.get_rect(center=(self.x + BIRD_W//2, self.y + BIRD_H//2))
                
                # Rotate bird based on speed
                angle = -self.speed * 2
                angle = max(-30, min(30, angle))  # Clamp angle between -30 and 30
                
                # Rotate the bird image
                rotated_bird = pygame.transform.rotate(bird_img, angle)
                rotated_rect = rotated_bird.get_rect(center=bird_rect.center)
                
                # Draw the bird
                screen.blit(rotated_bird, rotated_rect.topleft)
            except Exception as e:
                # Fallback to simple draw if rotation fails
                screen.blit(bird_img, (self.x, self.y))
                print(f"Error drawing bird: {e}")

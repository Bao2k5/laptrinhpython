import numpy as np
from AI.neural_network import NeuralNetwork

BIRD_W = 40
BIRD_H = 30

class BirdAI:
    def __init__(self, brain=None, load_best=False):
        self.x = 50
        self.y = 300
        self.speed = 0
        self.dead = False
        self.score = 0

        if load_best:
            self.brain = NeuralNetwork()
            try:
                self.brain.load("ai_best_model.npz")
                print("Loaded best AI model!")
            except:
                print("No best model found, using random brain.")
        else:
            if brain is not None:
                self.brain = brain.clone()
                self.brain.mutate(0.1)
            else:
                self.brain = NeuralNetwork()

    def update(self, pipes, gravity, jump_force, gap, height, pipe_width=80):
        if self.dead:
            return

        self.speed += gravity
        self.y += self.speed

        self.score += 1

        nearest = None
        for p in pipes:
            if p["x"] + pipe_width >= self.x:
                nearest = p
                break

        if nearest is None:
            if self.y < 0 or self.y + BIRD_H > height:
                self.dead = True
            return

        dx = (nearest["x"] - self.x) / 500.0
        dy_top = (nearest["gap_y"] - self.y) / height
        dy_bottom = (nearest["gap_y"] + gap - self.y) / height

        inputs = np.array([dx, dy_top, dy_bottom])

        output = self.brain.forward(inputs)
        if output > 0.5:
            self.speed = jump_force

        if self.y < 0 or self.y + BIRD_H > height:
            self.dead = True
            return

        in_x_range = (self.x + BIRD_W > nearest["x"]) and (self.x < nearest["x"] + pipe_width)
        in_gap = (self.y > nearest["gap_y"]) and (self.y + BIRD_H < nearest["gap_y"] + gap)

        if in_x_range and not in_gap:
            self.dead = True

    def draw(self, screen, bird_img):
        screen.blit(bird_img, (self.x, self.y))

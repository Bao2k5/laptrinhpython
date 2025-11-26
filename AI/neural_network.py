import numpy as np
import random

class NeuralNetwork:
    def __init__(self, input_size=5, hidden_size=6, output_size=1):
        # Initialize weights with Xavier/Glorot initialization
        limit1 = np.sqrt(6 / (input_size + hidden_size))
        limit2 = np.sqrt(6 / (hidden_size + output_size))
        
        self.w1 = np.random.uniform(-limit1, limit1, (input_size, hidden_size))
        self.w2 = np.random.uniform(-limit2, limit2, (hidden_size, output_size))
        self.fitness = 0

    def forward(self, inputs):
        # Forward pass with tanh activation for hidden layer
        h = np.tanh(np.dot(inputs, self.w1))
        # Sigmoid activation for output
        out = 1 / (1 + np.exp(-np.dot(h, self.w2)))
        return out[0]

    def mutate(self, rate=0.1):
        # More controlled mutation using normal distribution
        mutation_mask1 = np.random.random(self.w1.shape) < rate
        mutation_mask2 = np.random.random(self.w2.shape) < rate
        
        self.w1 += np.random.normal(0, 0.5, self.w1.shape) * mutation_mask1
        self.w2 += np.random.normal(0, 0.5, self.w2.shape) * mutation_mask2
        
        # Clip weights to prevent explosion
        self.w1 = np.clip(self.w1, -5, 5)
        self.w2 = np.clip(self.w2, -5, 5)

    def clone(self):
        nn = NeuralNetwork()
        nn.w1 = self.w1.copy()
        nn.w2 = self.w2.copy()
        nn.fitness = self.fitness
        return nn

    def crossover(self, partner):
        # Create child with crossover from two parents
        child = NeuralNetwork()
        
        # Perform crossover on weights
        for i in range(self.w1.shape[0]):
            for j in range(self.w1.shape[1]):
                if random.random() > 0.5:
                    child.w1[i][j] = self.w1[i][j]
                else:
                    child.w1[i][j] = partner.w1[i][j]
        
        for i in range(self.w2.shape[0]):
            for j in range(self.w2.shape[1]):
                if random.random() > 0.5:
                    child.w2[i][j] = self.w2[i][j]
                else:
                    child.w2[i][j] = partner.w2[i][j]
        
        return child

    def save(self, filename="ai_best_model.npz"):
        np.savez(filename, w1=self.w1, w2=self.w2)

    def load(self, filename="ai_best_model.npz"):
        try:
            data = np.load(filename)
            w1 = data["w1"]
            w2 = data["w2"]

            # Nếu shape không khớp (ví dụ version cũ dùng 3 input thay vì 5)
            # thì bỏ qua model cũ để tránh lỗi dot product
            if w1.shape != self.w1.shape or w2.shape != self.w2.shape:
                print("Saved model shape mismatch, using random weights")
                return False

            self.w1 = w1
            self.w2 = w2
            return True
        except Exception:
            print("Failed to load model, using random weights")
            return False

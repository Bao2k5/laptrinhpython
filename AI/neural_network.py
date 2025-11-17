import numpy as np

class NeuralNetwork:
    def __init__(self, input_size=3, hidden_size=6, output_size=1):
        self.w1 = np.random.randn(input_size, hidden_size)
        self.w2 = np.random.randn(hidden_size, output_size)

    def forward(self, inputs):
        h = np.tanh(np.dot(inputs, self.w1))
        out = 1 / (1 + np.exp(-np.dot(h, self.w2)))
        return out[0]

    def mutate(self, rate=0.1):
        self.w1 += np.random.randn(*self.w1.shape) * rate
        self.w2 += np.random.randn(*self.w2.shape) * rate

    def clone(self):
        nn = NeuralNetwork()
        nn.w1 = self.w1.copy()
        nn.w2 = self.w2.copy()
        return nn

    def save(self, filename="ai_best_model.npz"):
        np.savez(filename, w1=self.w1, w2=self.w2)

    def load(self, filename="ai_best_model.npz"):
        data = np.load(filename)
        self.w1 = data["w1"]
        self.w2 = data["w2"]

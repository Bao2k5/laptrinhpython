import json
import os
import numpy as np
from AI.neural_network import NeuralNetwork

MODEL_FILE = "ai_best_model.json"

def save_model(brain, filename=MODEL_FILE):
    data = {
        "w1": brain.w1.tolist(),
        "w2": brain.w2.tolist()
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f)

def load_model(filename=MODEL_FILE):
    if not os.path.exists(filename):
        return None

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    nn = NeuralNetwork()
    nn.w1 = np.array(data["w1"])
    nn.w2 = np.array(data["w2"])
    return nn

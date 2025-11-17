import random
from AI.bird_ai import BirdAI

def next_generation(birds, population=50):
    birds_sorted = sorted(birds, key=lambda b: b.score, reverse=True)

    # SAVE BEST MODEL
    best_bird = birds_sorted[0]
    best_bird.brain.save("ai_best_model.npz")
    print(">>> Saved best AI model!")

    elite_count = max(1, population // 5)
    elite = birds_sorted[:elite_count]

    new_birds = []
    for _ in range(population):
        parent = random.choice(elite)
        new_birds.append(BirdAI(parent.brain))

    return new_birds
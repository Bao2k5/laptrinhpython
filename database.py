import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["flappy_game"]
users_col = db["users"]
scores_col = db["scores"]

# USER
def create_user(username, password):
    if users_col.find_one({"username": username}):
        return False
    users_col.insert_one({"username": username, "password": password})
    return True

def check_login(username, password):
    return users_col.find_one({"username": username, "password": password}) is not None

# SCORE
def save_score(username, score):
    old = scores_col.find_one({"username": username})

    if old:
        if score > old.get("score", 0):
            scores_col.update_one(
                {"username": username},
                {"$set": {"score": score}}
            )
    else:
        scores_col.insert_one({"username": username, "score": score})


def get_top_scores(limit=10):
    return list(scores_col.find().sort("score", -1).limit(limit))

import os
from utils import in_browser, web_login, web_register, send_score_to_server

# Conditional import for PyMongo (Server-side only)
if not in_browser():
    from pymongo import MongoClient
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Bao:250905@cluster0.ifm5fiy.mongodb.net/flappybird?appName=Cluster0")
    client = MongoClient(MONGO_URI)
    db = client["flappy_game"]
    users_col = db["users"]
    scores_col = db["scores"]
else:
    # Browser mode: No direct DB access
    client = None
    db = None
    users_col = None
    scores_col = None

# USER
def create_user(username, password):
    if in_browser():
        return web_register(username, password)
    
    if users_col.find_one({"username": username}):
        return False
    users_col.insert_one({"username": username, "password": password})
    return True

def check_login(username, password):
    if in_browser():
        return web_login(username, password)

    return users_col.find_one({"username": username, "password": password}) is not None

# SCORE
def save_score(username, score):
    if in_browser():
        send_score_to_server(username, score)
        return

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
    if in_browser():
        # Fetch from API (async in sync context is hard, returning empty or cached)
        # For now, return empty list or implement sync XHR in utils if needed
        # But scores scene usually calls this.
        # Let's use a sync XHR for get_scores too if possible, or just return []
        try:
            from js import XMLHttpRequest, JSON
            xhr = XMLHttpRequest.new()
            xhr.open("GET", "/api/scores", False)
            xhr.send(None)
            if xhr.status == 200:
                return JSON.parse(xhr.responseText)
        except:
            pass
        return []

    return list(scores_col.find({}, {"_id": 0}).sort("score", -1).limit(limit))

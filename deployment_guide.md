# Deployment Guide

## Option 1: GitHub Pages (Static - No Shared Scores)
*Best for: Simple hosting, no cost, no database setup.*
*Limitation: High scores are only saved locally on the player's device.*

1.  **Upload Code**: Push your code to GitHub.
2.  **Deploy**: Go to Settings > Pages, select `gh-pages` branch (or `master` /root).
3.  **Play**: Visit your `github.io` link.

---

## Option 2: Render (Dynamic - Shared Scores)
*Best for: Multiplayer features, shared high scores.*
*Requirement: A Render account and a MongoDB database.*

### 1. Prepare MongoDB
You need a cloud database. **MongoDB Atlas** is a good free option.
1.  Create an account on [MongoDB Atlas](https://www.mongodb.com/atlas).
2.  Create a free cluster.
3.  Get your **Connection String** (URI). It looks like: `mongodb+srv://<user>:<password>@cluster0.mongodb.net/...`

### 2. Deploy to Render
1.  Create an account on [Render.com](https://render.com).
2.  Click **New +** and select **Web Service**.
3.  Connect your GitHub repository.
4.  **Settings**:
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn app:app`
5.  **Environment Variables** (Important!):
    *   Key: `MONGO_URI`
    *   Value: (Paste your MongoDB Connection String here)
6.  Click **Create Web Service**.

### 3. Play!
Render will give you a URL (e.g., `https://flappy-bird.onrender.com`).
Everyone playing on this URL will share the same High Score board!

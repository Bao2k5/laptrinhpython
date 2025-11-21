from flask import Flask, request, jsonify, send_from_directory
import os
from database import save_score, get_top_scores

# Lấy đường dẫn tuyệt đối đến thư mục build/web
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, 'build', 'web')

app = Flask(__name__, static_folder=STATIC_FOLDER)

@app.route('/')
def index():
    # Serve the main HTML file from the build/web directory
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    # Serve other static files (apk, js, etc.)
    return send_from_directory(app.static_folder, path)

@app.route('/api/scores', methods=['GET'])
def get_scores():
    scores = get_top_scores()
    return jsonify(scores)

@app.route('/api/score', methods=['POST'])
def post_score():
    data = request.json
    username = data.get('username')
    score = data.get('score')
    
    if username and score is not None:
        save_score(username, score)
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Invalid data"}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    from database import check_login
    if check_login(username, password):
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    from database import create_user
    if create_user(username, password):
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "User already exists"}), 400

if __name__ == '__main__':
    app.run(debug=True)

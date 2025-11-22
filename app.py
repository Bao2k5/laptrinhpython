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

@app.route('/debug/check-files')
def debug_check_files():
    """Debug endpoint to check if build files exist"""
    import os
    result = {
        "static_folder": app.static_folder,
        "base_dir": BASE_DIR,
        "files_in_static": []
    }
    try:
        if os.path.exists(app.static_folder):
            result["static_folder_exists"] = True
            result["files_in_static"] = os.listdir(app.static_folder)
        else:
            result["static_folder_exists"] = False
    except Exception as e:
        result["error"] = str(e)
    return jsonify(result)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        # Get stats using database functions
        scores = get_top_scores(limit=1)  # Get top score
        highest_score = scores[0]['score'] if scores else 0
        
        # Count total players by getting all scores
        all_scores = get_top_scores(limit=1000)  # Get more to count
        total_players = len(all_scores)
        total_games = total_players  # Simplified: assume 1 game per player
        
        return jsonify({
            'total_players': total_players,
            'total_games': total_games,
            'highest_score': highest_score
        })
    except Exception as e:
        # Return zeros if error
        return jsonify({
            'total_players': 0,
            'total_games': 0,
            'highest_score': 0
        })

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

# Catch-all route for static files - MUST be last to not interfere with API routes
@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory(app.static_folder, path)
    except:
        # If file not found, return 404
        return "File not found", 404


if __name__ == '__main__':
    app.run(debug=True)

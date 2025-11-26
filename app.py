from flask import Flask, send_from_directory, request, jsonify
import json
import os
from datetime import datetime

# Minimal WSGI app used for deployments
# Serves the static website from the 'website' folder
app = Flask(__name__, static_folder='website', static_url_path='')

# Path to scores JSON file
SCORES_FILE = 'scores.json'

def load_scores():
    """Load scores from JSON file"""
    if not os.path.exists(SCORES_FILE):
        return []
    try:
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_scores(scores):
    """Save scores to JSON file"""
    try:
        with open(SCORES_FILE, 'w') as f:
            json.dump(scores, f, indent=2)
        return True
    except:
        return False

@app.route('/')
def index():
    return send_from_directory('website', 'index.html')

@app.route('/api/score', methods=['POST'])
def submit_score():
    """Receive score from desktop game"""
    try:
        data = request.get_json()
        username = data.get('username')
        score = data.get('score')
        device_id = data.get('device_id')
        
        if not username or score is None:
            return jsonify({'error': 'Missing username or score'}), 400
        
        scores = load_scores()
        
        # Find existing entry by device_id or username
        existing = None
        if device_id:
            existing = next((s for s in scores if s.get('device_id') == device_id), None)
        if not existing:
            existing = next((s for s in scores if s.get('username') == username), None)
        
        if existing:
            # Update if new score is higher
            if score > existing.get('score', 0):
                existing['score'] = score
                existing['username'] = username
                existing['updated_at'] = datetime.now().isoformat()
                if device_id:
                    existing['device_id'] = device_id
        else:
            # Add new entry
            new_entry = {
                'username': username,
                'score': score,
                'device_id': device_id,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            scores.append(new_entry)
        
        save_scores(scores)
        return jsonify({'success': True}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scores', methods=['GET'])
def get_scores():
    """Return top scores for leaderboard"""
    try:
        limit = request.args.get('limit', 10, type=int)
        scores = load_scores()
        
        # Sort by score descending
        sorted_scores = sorted(scores, key=lambda x: x.get('score', 0), reverse=True)
        
        # Return top N with only necessary fields
        top_scores = [
            {
                'username': s.get('username'),
                'score': s.get('score')
            }
            for s in sorted_scores[:limit]
        ]
        
        return jsonify(top_scores), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Return statistics for website hero section"""
    try:
        scores = load_scores()
        
        # Calculate stats
        total_players = len(scores)
        highest_score = max([s.get('score', 0) for s in scores]) if scores else 0
        
        # For total_games, we'll use total_players as proxy since we don't track individual games
        # You could add a 'games_played' field to each player entry if needed
        total_games = total_players  # Simplified - each player = 1 game for now
        
        return jsonify({
            'total_players': total_players,
            'total_games': total_games,
            'highest_score': highest_score
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

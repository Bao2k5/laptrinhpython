from flask import Flask, render_template, request, jsonify, Response, session, redirect, url_for
import pygame
import sys
import io
import base64
from PIL import Image
import numpy as np
import threading
import time
from database import create_user, check_login, save_score, get_top_scores
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-12345'  # Fixed secret key

# Pygame setup (chạy 1 lần)
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Headless mode for server
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # Hide pygame messages

try:
    pygame.init()
    pygame.display.set_mode((1, 1))  # Dummy display for headless
    pygame.font.init()  # Initialize fonts
except Exception as e:
    print(f"Pygame init error: {e}")

# Game dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.Surface((WIDTH, HEIGHT))  # Create surface for rendering

# Game variables
bird = pygame.Rect(50, 300, 30, 25)
bird_speed = 0
gravity = 0.5
jump_force = -8

pipes = []
score = 0
game_over = False
game_started = False

pipe_width = 60
pipe_gap = 150
pipe_speed = 2

colors = {
    'background': (112, 197, 206),
    'bird': (247, 211, 84),
    'pipe': (115, 199, 103),
    'text': (255, 255, 255)
}

def reset_game():
    global bird, bird_speed, pipes, score, game_over, game_started
    bird = pygame.Rect(50, 300, 30, 25)
    bird_speed = 0
    pipes = []
    score = 0
    game_over = False
    game_started = False

def endGame():
    global game_over, score
    game_over = True
    # Lưu điểm số nếu có user đăng nhập
    if 'username' in session:
        username = session['username']
        save_score(username, score)

def jump():
    global bird_speed, game_started
    if not game_started:
        game_started = True
    bird_speed = jump_force

def update_game():
    global bird_speed, pipes, score, game_over
    
    if game_over or not game_started:
        return
    
    # Update bird
    bird_speed += gravity
    bird.y += int(bird_speed)
    
    # Check boundaries
    if bird.y < 0 or bird.y + bird.height > HEIGHT:
        endGame()
        return
    
    # Update pipes
    if len(pipes) == 0 or pipes[-1]['x'] < WIDTH - 200:
        pipe_height = np.random.randint(50, HEIGHT - pipe_gap - 50)
        pipes.append({
            'x': WIDTH,
            'top_height': pipe_height,
            'passed': False
        })
    
    # Move pipes and check collisions
    for i in range(len(pipes) - 1, -1, -1):
        pipe = pipes[i]
        pipe['x'] -= pipe_speed
        
        # Remove off-screen pipes
        if pipe['x'] + pipe_width < 0:
            pipes.pop(i)
            continue
        
        # Check collision
        bird_rect = pygame.Rect(bird.x, bird.y, bird.width, bird.height)
        top_pipe_rect = pygame.Rect(pipe['x'], 0, pipe_width, pipe['top_height'])
        bottom_pipe_rect = pygame.Rect(pipe['x'], pipe['top_height'] + pipe_gap, pipe_width, HEIGHT - pipe['top_height'] - pipe_gap)
        
        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            endGame()
            return
        
        # Update score
        if not pipe['passed'] and pipe['x'] + pipe_width < bird.x:
            pipe['passed'] = True
            score += 1

def draw_game():
    # Clear screen
    screen.fill(colors['background'])
    
    # Draw bird
    pygame.draw.rect(screen, colors['bird'], bird)
    
    # Draw pipes
    for pipe in pipes:
        # Top pipe
        pygame.draw.rect(screen, colors['pipe'], (pipe['x'], 0, pipe_width, pipe['top_height']))
        # Bottom pipe
        pygame.draw.rect(screen, colors['pipe'], (pipe['x'], pipe['top_height'] + pipe_gap, pipe_width, HEIGHT - pipe['top_height'] - pipe_gap))
    
    # Draw score
    try:
        font = pygame.font.Font(None, 36)
        score_text = font.render(str(score), True, colors['text'])
        screen.blit(score_text, (20, 20))
    except:
        pass
    
    # Draw start message
    if not game_started:
        try:
            font = pygame.font.Font(None, 24)
            start_text = font.render("Nhấn SPACE để bắt đầu", True, colors['text'])
            text_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(start_text, text_rect)
        except:
            pass
    
    # Draw game over message
    if game_over:
        # Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        try:
            font = pygame.font.Font(None, 48)
            game_over_text = font.render("GAME OVER", True, colors['text'])
            text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            screen.blit(game_over_text, text_rect)
            
            font = pygame.font.Font(None, 24)
            score_text = font.render(f"Điểm: {score}", True, colors['text'])
            text_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(score_text, text_rect)
            
            restart_text = font.render("Nhấn R để chơi lại", True, colors['text'])
            text_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
            screen.blit(restart_text, text_rect)
        except:
            pass

def game_loop():
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump()
                elif event.key == pygame.K_r and game_over:
                    reset_game()
        
        update_game()
        draw_game()
        clock.tick(60)

@app.route('/test')
def test():
    return "Server is working!"

@app.route('/')
def index():
    if 'username' in session:
        return render_template('web_game.html', username=session['username'])
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(f"Login attempt: {data}")  # Debug
        username = data.get('username')
        password = data.get('password')
        
        if check_login(username, password):
            session['username'] = username
            print(f"Login successful for {username}")  # Debug
            return jsonify({'success': True})
        else:
            print(f"Login failed for {username}")  # Debug
            return jsonify({'success': False, 'message': 'Tên đăng nhập hoặc mật khẩu không đúng'})
    except Exception as e:
        print(f"Login error: {e}")  # Debug
        return jsonify({'success': False, 'message': f'Lỗi: {str(e)}'})

@app.route('/register')
def register_page():
    if 'username' in session:
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print(f"Register attempt: {data}")  # Debug
        username = data.get('username')
        password = data.get('password')
        
        if create_user(username, password):
            session['username'] = username
            print(f"Register successful for {username}")  # Debug
            return jsonify({'success': True})
        else:
            print(f"Register failed for {username}")  # Debug
            return jsonify({'success': False, 'message': 'Tên đăng nhập đã tồn tại'})
    except Exception as e:
        print(f"Register error: {e}")  # Debug
        return jsonify({'success': False, 'message': f'Lỗi: {str(e)}'})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/web_game')
def web_game():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('web_game.html', username=session['username'])

@app.route('/game_frame')
def game_frame():
    # Chạy game loop trong thread riêng
    def run_game():
        game_loop()
    
    game_thread = threading.Thread(target=run_game)
    game_thread.daemon = True
    game_thread.start()
    
    return "Game started"

@app.route('/game_image')
def game_image():
    # Lấy screenshot của game
    try:
        # Chuyển pygame surface thành PIL Image
        img_str = pygame.image.tostring(screen, 'RGB')
        img = Image.frombytes('RGB', (WIDTH, HEIGHT), img_str)
        
        # Chuyển thành bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        return Response(img_byte_arr, mimetype='image/png')
    except:
        # Return placeholder if game not ready
        return Response("Game not ready", status=503)

@app.route('/jump', methods=['POST'])
def jump_action():
    jump()
    return jsonify({'success': True})

@app.route('/reset', methods=['POST'])
def reset_action():
    reset_game()
    return jsonify({'success': True})

@app.route('/scores')
def scores():
    if 'username' not in session:
        return redirect(url_for('index'))
    top_scores = get_top_scores(10)
    return render_template('scores.html', username=session['username'], scores=top_scores)

@app.route('/get_score')
def get_score():
    return jsonify({'score': score, 'game_over': game_over})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

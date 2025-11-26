from flask import Flask, render_template

# Minimal WSGI app used for deployments (avoids importing pygame/desktop code)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('web_game.html') if app.template_folder else 'Flappy Bird Web'

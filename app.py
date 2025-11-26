from flask import Flask, send_from_directory

# Minimal WSGI app used for deployments
# Serves the static website from the 'website' folder
app = Flask(__name__, static_folder='website', static_url_path='')

@app.route('/')
def index():
    return send_from_directory('website', 'index.html')

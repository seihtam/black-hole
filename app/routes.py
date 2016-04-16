from flask import render_template
from app import app, db, login_manager

# index
@app.route('/')
def index():
    return render_template('index.html')

# game
@app.route('/game')
def game():
    return render_template('game.html')

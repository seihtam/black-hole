from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import login_required, login_user, logout_user
from app import app, db, login_manager
from app.models import User

FLASH_ERROR = 'danger'
FLASH_SUCCESS = 'success'


# Set user loader
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter_by(id = int(user_id)).first()


# Index
@app.route('/')
def index():
    return render_template('index.html')


# game
@app.route('/game')
@login_required
def game():
    return render_template('game.html')


# rules
@app.route('/rules')
def rules():
    return render_template('rules.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # Validate user password
    username = request.form['username']
    password = request.form['password']
    user = db.session.query(User).filter_by(username = username).first()
    if not user or not user.check_password(password):
        flash('Invalid username or password', FLASH_ERROR)
        return redirect(url_for('login'))

    # Login user
    login_user(user)
    return redirect(url_for('index'))


# Logout
@app.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out', FLASH_SUCCESS)
    return redirect(url_for('index'))


# Create user
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    # Validate input
    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']
    if password1 == '' or username == '':
        flash('Enter a username and password', FLASH_ERROR)
        return redirect(url_for('signup'))
    if password1 != password2:
        flash('Passwords not matching', FLASH_ERROR)
        return redirect(url_for('signup'))

    # Create user
    try:
        user = User(username, password1)
        db.session.add(user)
        db.session.commit()
    except:
        # Solid error handling
        flash('User exists', FLASH_ERROR)
        return redirect(url_for('signup'))


    # Redirect login
    flash('User created, please login', FLASH_SUCCESS)
    return redirect(url_for('login'))


# Show scoreboard
@app.route('/score', methods=['GET'])
@login_required
def scoreboard():
    users = db.session.query(User).order_by(User.score.desc()).limit(100)
    return render_template('scoreboard.html', users=users)

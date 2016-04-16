from flask import render_template, flash, redirect, url_for, request
from app import app, db, login_manager
from sqlalchemy import func
from app.models import User


# Index
@app.route('/')
def index():
    return render_template('index.html')

# Login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # Validate user password
    username = request.form['username']
    password = request.form['password']
    user = db.session.query(User).filter(func.lower(User.username) == username.lower).first()
    if not user or not user.check_password(password):
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))

    # Login user
    login_user(user)
    return redirect(url_for('index'))

# Create user
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return render_template('signup.html')

    # Create user
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    db.session.add(user)

    # Redirect login
    flash('User created, please login', 'success')
    return redirect(url_for('login'))

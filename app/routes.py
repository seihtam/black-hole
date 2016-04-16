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
    user = db.session.query(User).filter_by(username = username).first()
    if not user or not user.check_password(password):
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))

    # Login user
    login_user(user)
    return redirect(url_for('index'))

# Create user
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    # Create user
    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']
    if password1 != password2:
        flash('Passwords not matching', 'error')
        return redirect(url_for('signup'))
    user = User(username, password1)
    db.session.add(user)

    # Redirect login
    flash('User created, please login', 'success')
    return redirect(url_for('login'))

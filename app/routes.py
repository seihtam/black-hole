from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import login_required, login_user
from app import app, db, login_manager
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

    # Validate input
    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']
    if password1 == '' or username == '':
        flash('Enter a username and password', 'error')
        return redirect(url_for('signup'))
    if password1 != password2:
        flash('Passwords not matching', 'error')
        return redirect(url_for('signup'))

    # Create user
    user = User(username, password1)
    db.session.add(user)
    db.session.commit()

    # Redirect login
    flash('User created, please login', 'success')
    return redirect(url_for('login'))

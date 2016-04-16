import os
from flask import Flask
from flask.ext.socketio import SocketIO
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

# Flask app
app = Flask(__name__)

# SocketIO
socketio = SocketIO()

# SQLAlchemy
db = SQLAlchemy()

# flask-login
login_manager = LoginManager()
login_manager.login_view = 'login'

def create_app(sqlalchemy_database_uri, debug=False):
    """Create an application."""
    # Set debug state
    app.debug = debug

    # Load secret key
    try:
        with open('secret', 'rb') as f:
            app.secret_key = f.read()
    except IOError:
        with open('secret', 'wb') as f:
            app.secret_key = os.urandom(32)
            f.write(app.secret_key)

    # Initialize flask-sqlalchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
    db.init_app(app)

    # Initialize SocketIO
    socketio.init_app(app)

    # Import routes and events
    from app import routes, events

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

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


def create_app(sqlalchemy_database_uri, debug=False):
    """Create an application."""
    # Set debug state
    app.debug = debug

    # Set secret_key
    app.secret_key = 'this_needs_to_be_replaced!'

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

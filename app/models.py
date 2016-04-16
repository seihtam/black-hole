from flask.ext.login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

DEFAULT_SCORE = 12000

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, username, password):
        self.score = DEFAULT_SCORE
        self.username = username
        self.set_password(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    # Flask-Login functions
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

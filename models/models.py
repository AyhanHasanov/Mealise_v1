from flask_login import UserMixin
from extensions import db

class User(db.Model, UserMixin):  # Inherit from UserMixin for Flask-Login
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    # Flask-Login methods
    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        # This can be used to check if the user is active or suspended
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True



class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), db.ForeignKey('user.username'), nullable=False)
    ingredients = db.Column(db.String(500), nullable=False)
    recipe = db.Column(db.String(1000), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
        return f'<Recipe {self.id} for {self.username}>'

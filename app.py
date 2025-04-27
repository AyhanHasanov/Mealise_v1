from flask import Flask
from dotenv import load_dotenv
import os
from flask_login import LoginManager
from extensions import db, bcrypt
from models.models import User
from routes.auth import auth_bp
from routes.discover import spoonacular_bp
from routes.home import home_bp
from routes.recipes import recipes_bp


load_dotenv()

def create_app():
    app = Flask(__name__)

    # Load environment variables and configure the app
    app.secret_key = os.getenv('FLASK_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(spoonacular_bp)

    # Initialize the extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)

    # Flask-Login Setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login page if not authenticated

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id) :
        return db.session.get(User, int(user_id))  # Updated method to avoid the legacy warning

    # Dynamically create the database tables if they don't exist
    with app.app_context():
        db.create_all()  # Ensure that the app context is set

    return app



if __name__ == "__main__":
    app = create_app()  # Create the app instance
    app.run(debug=True)

from flask import Blueprint, render_template

# Create a Blueprint for the home routes
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def landing():
    return render_template('landing.html')
#"Landing page"#render_template('landing.html')

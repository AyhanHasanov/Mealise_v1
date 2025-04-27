from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response
from flask_login import login_user, login_required, logout_user, current_user
from extensions import db, bcrypt
from models.models import User 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validations
        if not username or not email or not password:
            flash('Username, email, and password are required', 'danger')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('auth.register'))

        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists', 'danger')
            return redirect(url_for('auth.register'))

        # Create new user and save to database
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Log the user in after registration
        login_user(new_user)

        flash('Registration successful! You are now logged in.', 'success')
        return redirect(url_for('recipes.gen_recipe_page'))  # Redirect to the recipes page after registration

    return render_template('register.html')  # Render the registration page


@auth_bp.route('/login', methods=['GET', 'POST'])
def login() :
    if request.method == 'POST' :
        username = request.form.get('username')
        password = request.form.get('password')

        #Debug statement to check if username and password are received
        #print(f"Login attempt with username: {username}")

        # Check if the user exists
        user = User.query.filter_by(username=username).first()

        if user :
            #Debug statement to check if user is found
            #print(f"User found: {user.username}")
            if bcrypt.check_password_hash(user.password, password) :
                # Log the user in
                login_user(user)
                flash('Login successful!', 'success')

                # Get the 'next' parameter from the URL (if any)
                next_page = request.args.get('next')

                # Redirect to the 'next' URL or a default page if 'next' is not set
                if next_page :
                    return redirect(next_page)
                else :
                    return redirect(url_for('recipes.gen_recipe_page'))  # Default page

        flash('Invalid credentials, please try again.', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


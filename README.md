# Mealise - Smart Recipe Generator

Mealise is a Flask-based web application that helps users discover and generate recipes based on their available ingredients. It combines user-generated content with external recipe APIs to provide a comprehensive cooking experience.

## Features

- **Recipe Generation**: Create custom recipes using AI based on available ingredients
- **Recipe Discovery**: Browse recipes from Spoonacular API with advanced filtering
- **User Authentication**: Secure registration and login system with password hashing
- **Recipe Management**: Save, view, and delete your generated recipes
- **Responsive Design**: Mobile-friendly interface with Bootstrap 5

## Project Structure
mealise/
├── app.py # Main application entry point
├── extensions.py # Flask extensions initialization
├── .env # Environment variables
├── database.db # SQLite database
│
├── instance/ # Instance-specific configuration
│
├── models/ # Database models
│ └── models.py # User and Recipe models
│
├── routes/ # Application routes
│ ├── auth.py # Authentication routes
│ ├── discover.py # Recipe discovery routes
│ ├── home.py # Home page routes
│ ├── recipes.py # Recipe generation routes
│ └── init.py # Routes module initialization
│
├── templates/ # HTML templates
│ ├── partials/ # Reusable components
│ ├── base.html # Base template
│ ├── discover.html # Recipe discovery page
│ ├── landing.html # Landing page
│ ├── login.html # Login page
│ ├── recipe_page.html # Recipe generation page
│ └── register.html # Registration page
│
└── venv/ # Virtual environment


## Technologies Used

- **Backend**: Python, Flask
- **Database**: SQLite, Flask-SQLAlchemy
- **Authentication**: Flask-Login, Flask-Bcrypt
- **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2 templating
- **APIs**: Spoonacular API, OpenRouter AI API
- **Other**: dotenv for environment variables

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mealise.git
   cd mealise
Create and activate a virtual environment:

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
Create a .env file with your environment variables:

FLASK_SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///instance/mealise.db
SPOONACULAR_API_KEY=your_spoonacular_key
OPENROUTER_API_KEY=your_openrouter_key
Run the application:

bash
flask run
API Integration
Mealise integrates with:

Spoonacular API for recipe discovery

OpenRouter AI API for recipe generation

Screenshots
(Add screenshots of the main pages here if available)

License
This project is licensed under the MIT License - see the LICENSE file for details.


This Markdown file provides a comprehensive overview of your project while keeping it concise and easy to read. You can customize it further by adding screenshots, more detailed setup instruct

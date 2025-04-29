# Mealise - Smart Recipe Generator

Mealise is a Flask-based web application that helps users discover and generate recipes based on their available ingredients. It combines user-generated content with external recipe APIs to provide a comprehensive cooking experience.

## 1. Tech Stack
- Python 3.x
- Flask
- Jinja2 (for templating)
- Flask-Login (user session management)
- Flask-Bcrypt (password hashing)
- Flask-SQLAlchemy (ORM)
- SQLite (default database)
- Bootstrap 5 (frontend styling)
- Spoonacular API (external recipe search)
- OpenAI via OpenRouter API (AI recipe generation)
- dotenv (for environment variable management)

## 2. Project Structure
```
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
```

## 3. How to Set Up the App

#### 1. Clone the Repository
```
$ git clone <your-repo-url>
$ cd mealise
```
#### 2. Create and Activate a Virtual Environment
**Linux/macOS:**
```
$ python3 -m venv venv
$ source venv/bin/activate
```
**Windows: **
```
> python -m venv venv
> venv\Scripts\activate
```
#### 3. Install Required Dependencies
(Ensure you are in the virtual environment)
```
$ pip install -r requirements.txt
```

#### 4. Set Up Environment Variables
Create a `.env` file in the root directory with the following content:
```
FLASK_SECRET_KEY=your_flask_secret_key  
DATABASE_URI=sqlite:///instance/mealise.db  
SPOONACULAR_API_KEY=your_spoonacular_api_key  
OPENROUTER_API_KEY=your_openrouter_api_key  
```
Make sure to replace the placeholders with your **actual keys**

#### 5. Run the Application
```
$ python app.py
```
Access the app at: http://127.0.0.1:5000/


## 4. Features
- **Recipe Generation**: Create custom recipes using AI based on available ingredients
- **Recipe Discovery**: Browse recipes from Spoonacular API with advanced filtering
- **User Authentication**: Secure registration and login system with password hashing
- **Recipe Management**: Save, view, and delete your generated recipes
- **Responsive Design**: Mobile-friendly interface with Bootstrap 5


## 5. Notes

- The app uses SQLite by default. You can switch to another DB by changing the `DATABASE_URI` in `.env`.
- Avoid pushing `.env` or `instance/mealise.db` to public repositories for security reasons.

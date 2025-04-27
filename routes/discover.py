from flask import Blueprint, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SPOONACULAR_API_KEY")

spoonacular_bp = Blueprint('spoonacular', __name__)

def fetch_recipes(page=1, query='', cuisine='', diet='', sort=''):
    offset = (page - 1) * 10
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "number": 10,
        "offset": offset,
        "addRecipeInformation": True,
        "apiKey": API_KEY,
        "query": query,
        "cuisine": cuisine,
        "diet": diet,
        "sort": sort
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])

@spoonacular_bp.route('/discover', methods=['GET', 'POST'])
def unified_discover():
    page = 1
    query = ''
    cuisine = ''
    diet = ''
    sort = ''

    if request.method == 'POST':
        query = request.form.get('query', '')
        cuisine = request.form.get('cuisine', '')
        diet = request.form.get('diet', '')
        sort = request.form.get('sort', '')

    recipes = fetch_recipes(page, query, cuisine, diet, sort)
    return render_template('discover.html', recipes=recipes, current_page=page, query=query, cuisine=cuisine, diet=diet, sort=sort)

@spoonacular_bp.route('/discover/load_more', methods=['GET'])
def load_more_recipes():
    page = int(request.args.get('page', 1))
    query = request.args.get('query', '')
    cuisine = request.args.get('cuisine', '')
    diet = request.args.get('diet', '')
    sort = request.args.get('sort', '')

    recipes = fetch_recipes(page, query, cuisine, diet, sort)
    return render_template('partials/_recipes.html', recipes=recipes)

from flask import Blueprint, render_template, request, redirect, url_for
import requests
import os
from dotenv import load_dotenv
from flask_login import current_user
from extensions import db
from models.models import SpoonacularRecipes

load_dotenv()
API_KEY = os.getenv("SPOONACULAR_API_KEY")

spoonacular_bp = Blueprint('spoonacular', __name__)

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

    # Reuse the recipe cards part of discover.html directly
    return render_template('discover.html', recipes=recipes, current_page=page, query=query, cuisine=cuisine, diet=diet, sort=sort, load_more=True)


# @spoonacular_bp.route('/save_recipe', methods=['POST'])
# def save_recipe():
#     user_id = current_user.id
#     recipe_id = request.form.get('recipe_id')
#
#     new_recipe = SpoonacularRecipes(
#         recipe_id=recipe_id,
#         user_id=user_id,
#     )
#
#     db.session.add(new_recipe)
#     db.session.commit()
#
#     return {'success': True}

@spoonacular_bp.route('/save_recipe', methods=['POST'])
def save_recipe():
    user_id = current_user.id
    recipe_id = request.form.get('recipe_id')

    # Check if already saved
    existing = SpoonacularRecipes.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if existing:
        return {'success': False, 'message': 'Recipe already saved.'}

    new_recipe = SpoonacularRecipes(
        recipe_id=recipe_id,
        user_id=user_id,
    )

    db.session.add(new_recipe)
    db.session.commit()

    return {'success': True, 'message': 'Recipe saved successfully!'}


@spoonacular_bp.route('/saved', methods=['GET'])
def view_saved_recipes():
    user_id = current_user.id
    page = int(request.args.get('page', 1))
    per_page = 9

    saved = SpoonacularRecipes.query.filter_by(user_id=user_id).all()
    recipe_ids = [str(entry.recipe_id) for entry in saved]

    if not recipe_ids:
        return render_template('saved.html', recipes=[], current_page=1, total_pages=1)

    total = len(recipe_ids)
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    page_ids = recipe_ids[start:end]

    url = "https://api.spoonacular.com/recipes/informationBulk"
    params = {
        "ids": ",".join(page_ids),
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)
    recipes = response.json()

    return render_template('saved.html', recipes=recipes, current_page=page, total_pages=total_pages)

@spoonacular_bp.route('/remove_recipe', methods=['POST'])
def remove_recipe():
    user_id = current_user.id
    recipe_id = request.form.get('recipe_id')

    saved = SpoonacularRecipes.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if saved:
        db.session.delete(saved)
        db.session.commit()
        return {'success': True}

    return {'success': False}, 404

def fetch_recipes(page=1, query='', cuisine='', diet='', sort=''):
    offset = (page - 1) * 9
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "number": 9,
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

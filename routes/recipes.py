from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from extensions import db
from models.models import Recipe
from openai import OpenAI
import os
from dotenv import load_dotenv
import re

recipes_bp = Blueprint('recipes', __name__)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

@recipes_bp.route('/recipes', methods=['GET'])
@login_required
def gen_recipe_page() :
    if not current_user.is_authenticated : 
        print("User not logged in, redirecting to login page...")
        return redirect(url_for('auth.login')) 

    username = current_user.username 

    # Import Recipe model here to avoid circular import
    from models.models import Recipe
    page = request.args.get('page', 1, type=int)
    per_page = 4
    recipes = Recipe.query.filter_by(username=username).order_by(Recipe.created_at.desc()).paginate(page=page, per_page=per_page)

    return render_template('recipe_page.html', recipes=recipes)



@recipes_bp.route('/generate_recipe', methods=['POST'])
def generate_and_save_recipe():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    ingredients = request.form['ingredients']
    raw_recipe_text = generate_recipe(ingredients)
    print(raw_recipe_text)

    parts = raw_recipe_text.split("$part-")
    title = ""
    parsed_ingredients = ""
    instructions = ""
    for part in parts :
        if part.startswith("title") :
            title = part.replace("title", "").strip()
        elif part.startswith("ingredients") :
            parsed_ingredients = part.replace("ingredients", "").strip()
        elif part.startswith("instructions") :
            instructions = part.replace("instructions", "").strip()

    print(title, ingredients, instructions)

    new_recipe = Recipe(
        username=current_user.username,
        ingredients=parsed_ingredients,
        recipe=instructions,
        title=title,
        created_at=db.func.current_timestamp()
    )
    db.session.add(new_recipe)
    db.session.commit()

    return redirect(url_for('recipes.gen_recipe_page'))  # Redirect to recipe page after saving the recipe

@recipes_bp.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    # Make sure the recipe belongs to the logged-in user
    if recipe.username != current_user.username:
        return "Unauthorized", 403

    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('recipes.gen_recipe_page'))


def generate_recipe(ingredients):
    prompt = f"""
You are a creative chef. Generate a recipe using the following ingredients: {ingredients}
You don't need to include ALL of the ingredients.
You can't use ingredients that are not in the list.
Format your answer exactly like this:

$part-title
[Insert a creative recipe title here]

$part-ingredients
-- ingredient 1
-- ingredient 2
-- ingredient 3

$part-instructions
1. Step one
2. Step two
3. Step three
"""

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

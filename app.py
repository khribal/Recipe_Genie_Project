from flask import Flask, render_template, request, jsonify
import requests 

app = Flask(__name__)

THEMEALDB_API_URL = "https://www.themealdb.com/api/json/v1/1"

def get_recipes_by_ingredient(ingredient):
    response = requests.get(f"{THEMEALDB_API_URL}/filter.php?i={ingredient}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_recipe_details(meal_id):
    response = requests.get(f"{THEMEALDB_API_URL}/lookup.php?i={meal_id}")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch recipe details")
    
def get_recipe_ingredients(meal_id):
    response = requests.get(f"{THEMEALDB_API_URL}/lookup.php?i={meal_id}")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch recipe details")
    
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recipes', methods=['POST'])
def recipes():
    data = request.get_json()
    user_message = data.get('message') if data else None

    if not user_message:
        return jsonify({'response': "No ingredient provided."}), 400

    ingredient = user_message
    recipes = get_recipes_by_ingredient(ingredient)

    if recipes and recipes['meals']:
        formatted_recipes = []
        for meal in recipes['meals'][:5]:
            meal_id = meal['idMeal']
            recipe_details = get_recipe_details(meal_id)
            if recipe_details and recipe_details['meals']:
                meal_info = recipe_details['meals'][0]

                # Gather ingredients
                ingredients = []
                for i in range(1, 21):  # Up to 20 ingredients
                    ingredient_name = meal_info.get(f'strIngredient{i}')
                    measure = meal_info.get(f'strMeasure{i}')
                    if ingredient_name and ingredient_name.strip():  # Only include if there's a name
                        ingredients.append(f"<li>{ingredient_name} ({measure})</li>")

                # Join the ingredients list into a single string
                ingredients_list = ''.join(ingredients)

                # Format recipe HTML
                recipe_html = f"""
                <div class="recipe">
                    <h3 class="recipe-title">{meal_info['strMeal']}</h3>
                    <p class="recipe-ingredients"><strong>Ingredients:</strong> <ul>{ingredients_list}</ul></p>
                    <p class="recipe-instructions"><strong>Instructions:</strong> {meal_info['strInstructions']}</p>
                </div>
                """
                formatted_recipes.append(recipe_html)

        # Join the formatted recipes without a comma separator
        return jsonify({'response': formatted_recipes})  # No need to join here, just return the list
    else:
        return jsonify({'response': "Sorry, I couldn't find any recipes for that ingredient."})

if __name__ == '__main__':
    app.run(debug=True)

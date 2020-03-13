from flask import Blueprint,jsonify,request
from models.user import User
from models.meal import Meal
from playhouse.shortcuts import model_to_dict


meal_api_blueprint = Blueprint('meal',
                             __name__,
                             template_folder='templates')


@meal_api_blueprint.route('/breakfast', methods = ['GET'])
def new_breakfast():

    food = Meal.select().where(Meal.meal == 'breakfast')
    food_data = []

    for f in food:
        info = {
            "label": f"{f.food} - {f.calories}kcal",
            "value": f.food
        }
        food_data.append(info)
    
    return jsonify(food_data), 200

@meal_api_blueprint.route('/lunch', methods = ['GET'])
def new_lunch():

    food = Meal.select().where(Meal.meal == 'lunch')
    food_data = []

    for f in food:
        info = {
            "label": f"{f.food} - {f.calories}kcal",
            "value": f.food
        }
        food_data.append(info)
    
    return jsonify(food_data), 200

@meal_api_blueprint.route('/dinner', methods = ['GET'])
def new_dinner():

    food = Meal.select().where(Meal.meal == 'dinner')
    food_data = []

    for f in food:
        info = {
            "label": f"{f.food} - {f.calories}kcal",
            "value": f.food
        }
        food_data.append(info)
    
    return jsonify(food_data), 200


@meal_api_blueprint.route('/create', methods = ['POST'])
def create():

    resp = request.get_json()
    meal = resp.get('meal')
    food = resp.get('food')
    calories = resp.get('calories')

    meal = Meal(meal = meal, food = food, calories = calories)

    if meal.save():
        message = {
            'status' : True,
            'message': 'created'
        }
    else:
        message = {
            'status' : False,
            'message': user.errors
        }

    return jsonify(message)


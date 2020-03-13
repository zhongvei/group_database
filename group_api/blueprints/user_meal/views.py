from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.user_meal import User_Meal
from models.meal import Meal

user_meal_api_blueprint = Blueprint('user_meal_api',
                             __name__,
                             template_folder='templates')

@user_meal_api_blueprint.route('/create', methods = ['POST'])
@jwt_required
def create():
    resp = request.get_json()

    current_user = get_jwt_identity()
    user = User.get_or_none(User.username == current_user)

    meal = Meal.get_or_none(Meal.food == resp['meal'])

    user_meal = User_Meal(user = user.id, meal = meal)

    if user_meal.save():
        message = {
            'status': True,
            'message': "Recorded meal",
            'info': {
                'name': meal.food,
                'calories': meal.calories
            }
        }
    else:
        message = {
            'status': False,
            'message': "Couldn't saved to database."
        }

    return jsonify(message)

@user_meal_api_blueprint.route('/',methods = ['GET'])
@jwt_required
def test():
    current_user = get_jwt_identity()
    
    user = User.get_or_none(User.username == current_user)
    
    arr = []

    for meal in user.meals:
        #havent solve today
        info = {
            'food': meal.meal.food,
            'calories': meal.meal.calories
        }
        arr.append(info)

    return jsonify(arr), 200
    







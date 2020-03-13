from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.user_meal import User_Meal
from models.meal import Meal
from datetime import date, datetime 

user_meal_api_blueprint = Blueprint('user_meal_api',
                             __name__,
                             template_folder='templates')

@user_meal_api_blueprint.route('/create', methods = ['POST'])
@jwt_required
def create():
    resp = request.get_json()

    current_user = get_jwt_identity()
    user = User.get_or_none(User.username == current_user)

    meal = Meal.get_or_none(Meal.food == resp['food'])

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
def view():
    current_user = get_jwt_identity()
    
    user = User.get_or_none(User.username == current_user)
    dic = {}
    user_arr = []
    meal_arr = []
    user_info = {
        'name': user.username
    }
    user_arr.append(user_info)
    for meal in user.meals:
        if meal.created_at == date.today():
            info = {
                'meal': meal.meal.meal,
                'food': meal.meal.food,
                'calories': meal.meal.calories
            }
            meal_arr.append(info)

    dic['user'] = user_arr
    dic['meal'] = meal_arr

    return jsonify(dic), 200

@user_meal_api_blueprint.route('/delete', methods = ['POST'])
@jwt_required
def delete():
    current_user = get_jwt_identity()
    user = User.get_or_none(User.username == current_user)
    resp = request.get_json()
    meal = Meal.get_or_none(Meal.food == resp['food'])
    user_meal = User_Meal.get_or_none((User_Meal.user_id == user.id) & (User_Meal.meal_id == meal.id))
    
    if user_meal:
        if user_meal.delete_instance():
            message = {
                'status': True,
                'message': "Successfully deleted from database"
            }
        else:
            message = {
                'status': False,
                'message': "Couldn't remove from database"
            }
    else:
        message = {
            'status': False,
            'message': "The meal submitted is not register with user"
        }

    return jsonify(message)







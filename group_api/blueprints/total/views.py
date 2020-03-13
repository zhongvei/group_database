from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_jwt_extended import jwt_required,  get_jwt_identity
from models.user import User
from models.user_activity import User_Activity
from models.user_meal import User_Meal
from datetime import date, datetime

total_api_blueprint = Blueprint('total', __name__, template_folder='templates')

@total_api_blueprint.route('/', methods = ['GET'])
@jwt_required
def view():
    current_user = get_jwt_identity()
    user = User.get_or_none(User.username == current_user)
    dic = {}
    user_arr = []
    meal_arr = []
    act_arr = []
    user_info = {
        'name': user.username
    }
    meal_count = 0
    meal_calories = 0
    act_count = 0
    act_calories = 0
    user_arr.append(user_info)
    for meal in user.meals:
        if meal.created_at == date.today():
            meal_count += 1
            meal_calories += meal.meal.calories
    info = {
        'count': meal_count,
        'calories': meal_calories
    }
    meal_arr.append(info)
    for activity in user.activity:
        if activity.created_at == date.today():
            act_count += 1
            act_calories += activity.activity.calories
    info = {
        'count': act_count,
        'calories': act_calories
    }
    act_arr.append(info)
    dic['meal'] = meal_arr
    dic['user'] = user_arr
    dic['activity']  = act_arr

    return jsonify(dic), 200
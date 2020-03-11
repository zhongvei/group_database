from flask import Blueprint,jsonify,request
from playhouse.shortcuts import model_to_dict

user_meal_api_blueprint = Blueprint('user_meal', 
                                 __name__, 
                                template_folder='templates')
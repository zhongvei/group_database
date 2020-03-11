from flask import Blueprint,jsonify,request
from playhouse.shortcuts import model_to_dict

user_activity_api_blueprint = Blueprint('user_activity', 
                                 __name__, 
                                template_folder='templates')
from flask import Blueprint,jsonify,request
from playhouse.shortcuts import model_to_dict

activity_api_blueprint = Blueprint('activity', 
                                 __name__, 
                                template_folder='templates')




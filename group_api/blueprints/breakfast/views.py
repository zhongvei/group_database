from flask import Blueprint,jsonify,request
from models.user import User
from playhouse.shortcuts import model_to_dict

breakfast_api_blueprint('breakfast_api',
                        __name__,
                        template_folder='templates')


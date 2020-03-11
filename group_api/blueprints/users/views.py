from flask import Blueprint, jsonify, request
from models.user import User
from playhouse.shortcuts import model_to_dict
from werkzeug.security import generate_password_hash,check_password_hash

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.select()
    user_data = []

    for user in users:
        user = model_to_dict(user)
        user_data.append(user)
    
    return jsonify(user_data), 200

@users_api_blueprint.route('/login', methods=['POST'])
def login():

    resp = request.get_json()
    username = resp.get('username')
    password = resp.get('password')

    user = User.get_or_none(User.username == username)

    if not user:
        message = {
            'status' : False,
            'message': 'Invalid post'
        }
    else:
        if check_password_hash(user.password, password):
            message = {
                'status' : True,
                'message': 'Successfully login!'
            }
        else:
            message = {
                'status' : False,
                'message': 'Invalid password'
            }
    
    return jsonify(message)


# @users_api_blueprint.route('/username', methods = ['GET'])
# def new():
#     if 'username' in request.args:
#         username = str(request.args['username'])
#     else:
#         user_data = {'error':'check your post'}
#         return jsonify(user_data)
#     user_data = []
#     user = User.get_or_none(User.name == username)
#     if not user:
#         user_data = {'error':'Not found'}
#         return jsonify(user_data)
#     user = model_to_dict(user)
#     user_data.append(user)
#     return jsonify(user_data), 200
    
@users_api_blueprint.route('/create', methods = ['POST'])
def create():

    resp = request.get_json()

    name = resp.get('name')
    username = resp.get('username')
    email = resp.get('email')
    password = resp.get('password')

    hashed_password = generate_password_hash(password)
    
    user = User(name = name, email = email, password = hashed_password, username = username)

    if user.save():
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


@users_api_blueprint.route('/<username>/edit', methods = ['POST'])
def edit(username):

    resp = request.get_json()
    user = User.get_or_none(User.username == username)

    age = resp.get('age')
    gender = resp.get('gender')
    weight = resp.get('weight')
    height = resp.get('height')
    
    user.age = age
    user.gender = gender
    user.weight = weight
    user.height = height

    if user.save():
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


from flask import Blueprint,jsonify,request
from playhouse.shortcuts import model_to_dict
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.user_activity import User_Activity
from models.activity import Activity

user_activity_api_blueprint = Blueprint('user_activity', 
                                 __name__, 
                                template_folder='templates')

@user_activity_api_blueprint.route('/create', methods= ['POST'])
@jwt_required
def create():
    resp = request.get_json()

    current_user = get_jwt_identity()
    user = User.get_or_none(User.username == current_user)

    activity = Activity.get_or_none(Activity.activity == resp['activity'])

    user_activity = User_Activity(user = user, activity = activity)

    if user_activity.save():
        message = {
            'status': True,
            'message': "Recorded activity",
            'info': {
                'activity': activity.activity,
                'calories': activity.calories
            }
        }
    else:
        message = {
            'status': False,
            'message': "Couldn't record to databsae"
        }

    return jsonify(message)

@user_activity_api_blueprint.route('/', methods = ['GET'])
@jwt_required
def view():
    current_user = get_jwt_identity()

    user = User.get_or_none(User.username == current_user)
    dic = {}
    user_arr = []
    act_arr = []
    user_info = {
        'name': user.username
    }
    user_arr.append(user_info)
    for activity in user.activity:
        info = {
            'activity': activity.activity.activity,
            'calories': activity.activity.calories
        }
        act_arr.append(info)
    dic['user'] = user_arr
    dic['activity'] = act_arr

    return jsonify(dic), 200

@user_activity_api_blueprint.route('/delete', methods = ['POST'])
@jwt_required
def delete():
    current_user = get_jwt_identity()
    
    user = User.get_or_none(User.username == current_user)

    resp = request.get_json()

    activity = Activity.get_or_none(Activity.activity == resp['activity'])

    user_activity = User_Activity.get_or_none((User_Activity.user_id == user.id) & (User_Activity.activity_id == activity.id))
    if user_activity:
        if user_activity.delete_instance():
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
            'message': "The activity submitted is not register with user"
        }

    return jsonify(message)
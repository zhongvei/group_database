from flask import Blueprint,jsonify,request
from playhouse.shortcuts import model_to_dict
from models.activity import Activity

activity_api_blueprint = Blueprint('activity', 
                                 __name__, 
                                template_folder='templates')

@activity_api_blueprint.route('/create', methods = ['POST'])
def create():

    resp = request.get_json()

    activity = resp['activity']
    calories = resp['calories']

    act = Activity(activity = activity, calories = calories)
    if act.save():
        message = {
            'status' : True,
            'message': 'created',
            'activity': {
                'activity': act.activity,
                'calories': act.calories
            }
        }
    else:
        message = {
            'status' : False,
            'message': "activity can't be created"
        }

    return jsonify(message)

@activity_api_blueprint.route('/', methods = ['GET'])
def new():

    activity = Activity.select()
    activity_data = []

    for act in activity:
        info = {
            'name': act.activity,
            'calories': act.calories
        }
        activity_data.append(info)

    return jsonify(activity_data)




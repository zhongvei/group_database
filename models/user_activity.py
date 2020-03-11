from base_model import BaseModel
import peewee as pw
from models.user import User
from models.activity import Activity

class User_Meal(BaseModel):

    user = pw.ForeignKeyField(User, backref='meals')
    activity = pw.Activity(Activity)

    def validate():
        return
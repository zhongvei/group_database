from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.meal import Meal
import datetime

class User_Meal(BaseModel):
    created_at = pw.DateField(default = datetime.datetime.today())
    user = pw.ForeignKeyField(User, backref='meals')
    meal = pw.ForeignKeyField(Meal, backref='user')

    def validate(self):
        return
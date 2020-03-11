from base_model import BaseModel
import peewee as pw
from models.user import User
from models.meal import Meal

class User_Meal(BaseModel):

    user = pw.ForeignKeyField(User, backref='meals')
    meal = pw.ForeignKeyField(Meal)

    def validate():
        return
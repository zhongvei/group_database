from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.activity import Activity

class User_Activity(BaseModel):

    user = pw.ForeignKeyField(User, backref='meals')
    activity = pw.ForeignKeyField(Activity)

    def validate():
        return
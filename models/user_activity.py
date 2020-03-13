from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.activity import Activity
import datetime

class User_Activity(BaseModel):
    created_at = pw.DateField(default = datetime.datetime.today())
    user = pw.ForeignKeyField(User, backref='activity')
    activity = pw.ForeignKeyField(Activity, backref='user')

    def validate(self):
        return
    
from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.user_images import Image

class Donations(BaseModel):
    amount = pw.DecimalField()
    image = pw.ForeignKeyField(Image, backref='donations')
    user = pw.ForeignKeyField(User, backref='donations')

    def validate(self):
        return
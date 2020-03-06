from models.base_model import BaseModel
import peewee as pw
from models.user import User


class Image(BaseModel):
    image_path = pw.CharField(null = True)
    user = pw.ForeignKeyField(User, backref='images')
    
    def validate(self):
        return

    def get_url(self):
        return 'https://pleaseletmeusethisbucketname.s3-ap-southeast-1.amazonaws.com/' + self.image_path
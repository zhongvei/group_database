from models.base_model import BaseModel
import peewee as pw

class Activity(BaseModel):
    activity = pw.CharField(unique = True)
    height = pw.IntegerField()

    def validate():
        return
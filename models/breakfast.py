from models.base_model import BaseModel
import peewee as peewee

class Breakfast(BaseModel):
    food = pw.CharField(unique = True)
    calories = pw.IntegerField()

    def validate(self):
        duplicate_food = Breakfast.get_or_none(Breakfast.food == self.food)
        if duplicate_food:
            self.errors.append('Food is already listed!')
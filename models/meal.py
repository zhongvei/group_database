from models.base_model import BaseModel
import peewee as pw

class Meal(BaseModel):

    meal = pw.CharField()
    food = pw.CharField(unique = True)
    calories = pw.IntegerField()

    def validate(self):
        duplicate_food = Meal.get_or_none(Meal.food == self.food)
        if duplicate_food:
            self.errors.append('Food is already listed!')
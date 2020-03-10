from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    name = pw.CharField(unique=False)
    username = pw.CharField(unique = True)
    email = pw.CharField(unique=True)
    gender = pw.CharField(null = True)
    age = pw.IntegerField(null = True)
    weight = pw.IntegerField(null = True)
    height = pw.IntegerField(null = True)
    password = pw.CharField()

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)
        if duplicate_username:
                self.errors.append('Username not unique')
        if duplicate_email:
                self.errors.append('Email not unique')





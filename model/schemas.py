from app import ma
from .models import *


class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_name","email")
        model = User

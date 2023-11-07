from shutil import unregister_unpack_format
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import User


class UserAuth(ModelBackend):
    def authenticate(phone=None, password=None):
        try:
            user = User.objects.get(phone=phone)
            if check_password(password, user.password):
                return user

            return None

        except Exception as e:
            # # print(e)
            return None
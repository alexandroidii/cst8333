from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

"""
Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19

This class and the authenticate method perform the case insentive backend to the user application and Users model.
The USERNAME_FIELD is specified in the Users model which USERNAME_FIELD = 'email'.

https://docs.djangoproject.com/en/3.1/topics/auth/customizing/
Based on https://youtu.be/SFarxlTzVX4?t=2072
"""

class CaseInsensitiveAuth(ModelBackend):
    def authenticate(self, request,username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
           username = kwargs.get(UserModel.USERNAME_FIELD) #get this field from custom user mode
        try:
            case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            user = UserModel._default_manager.get(**{case_insensitive_username_field:username}) #python majic - getting user based on email field
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            pass
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
  
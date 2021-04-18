from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


'''
https://docs.djangoproject.com/en/3.1/topics/auth/customizing/
Based on https://youtu.be/SFarxlTzVX4?t=2072
'''
class CaseInsensitiveAuth(ModelBackend):
    def authenticate(self, request,username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
           username = kwargs.get(UserModel.USERNAME_FIELD) #get this field from custom user mode
        try:
            case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            user = UserModel._default_manager.get(**{case_insensitive_username_field:username}) #python majic
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            pass
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
  
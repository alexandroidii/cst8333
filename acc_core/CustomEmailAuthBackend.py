from django.contrib.auth.models import User
'''
class EmailAuthBackend(ModelBackend):
    
    def authenticate(self,request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
           username = kwargs.get(UserModel.USERNAME_FIELD) #get this field from custom user mode
        print('test')
        try:
            case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            user = UserModel._default_manager.get(**{case_insensitive_username_field:username}) #python majic
        except: UserModel.DoesNotExist
           # UserModel().set_password(password)
           # pass
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
'''
class EmailAuthBackend():
    def authenticate(self, request, username, password):
        try:
            user = User.objects.get(email=username)
            success = user.check_password(password)
            if success:
                return user
        except User.DoesNotExist:
                pass
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None 

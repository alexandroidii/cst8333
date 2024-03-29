# import  rlcs.models
import rlcs.models_dropdown as dropDowns

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in
from phone_field import PhoneField
from django.apps import apps

"""
Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19

A custom Users model was created since the default Django auth framework users user_name and not email address as a unique identifying field
of the user. Users would more easily remember their email addresses.

The model enties are described in the Users class which extends from both the AbstractBaseUser and PermissionsMixin as a requirement within
a custom users model. The default PermissionMixin utilizes the permission facility within the permission framework that Django has.
is_superuser is one example of the PermissionMixin framework used. It is for this reason there is no entity in the model class.

A CustomAccountManage extends BaseUserManager so that we utilize create_user and create_superuser. By doing so, this instructs Django that
we are utilizing more fields than what is defined in the authentication table.

Create_user function: Are the required fields when a user signs up (email, user_name, first_name, last_name, password). A couple validations
    are performed to instruct the user that they must provide an email and username. is_active is set false by default which then is set true
    during the user registration/validation process.

Create_superuser function: A superuser must also input the required fields (email, user_name, first_name, last_name, password).
    As an example when you create a superuser for the first time using python manage.py createsusperuser, the user will be prompted
    to enter these required fields. is_staff and is_superuser must be set true and are handled within this method. is_active must be set True
    or you will never be able to log into the system. To summmarize, in order to log into the system as a superuser all three fields must be
    set true - is_staff, is_superuser, is_active. Furthermore, you cannot log in as a superuser if is_staff is not true as well.

  
Ref:https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model/
https://youtu.be/Ae7nc1EGv-A
"""

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, last_name,  password, **other_fields):
       
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, last_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_active', False)

        if other_fields.get('is_active') is not True:
            raise ValueError(
                'User must be assigned to is_active=True.')

        if not email:
            raise ValueError(_('You must provide an email address'))
        if not user_name:
            raise ValueError(_('You must provide a username'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    

class Users(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(_('first name'), max_length=25)
    last_name = models.CharField(_('last name'), max_length=25)
    phone_number = PhoneField(_('phone number'), max_length=25, blank=True) #changed from CharField to PhoneField
    company_name = models.CharField(_('company name'),max_length=50, blank=True)
    industry_type = models.ForeignKey(dropDowns.IndustryType, models.SET_NULL, blank=True, null=True)
    position = models.CharField(_('position'),max_length=50, blank=True)
    website = models.CharField(_('website'), max_length=50, blank=True)
    address = models.CharField(_('address'),max_length=50, blank=True)
    city = models.CharField(_('city'), max_length=50, blank=True)
    province_state = models.CharField(_('province'), max_length=20, blank=True)
    country = models.CharField(_('country'), max_length=20, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_reviewer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


    class Meta: 
        verbose_name_plural = "CCS Users" #define the name of model displayed. Otherwise Users will be displayed

    objects = CustomAccountManager()    #define we are using customaccountmanager above 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name'] #shows up with py manage.py createsuperuser

    def __str__(self):
        return self.user_name

    """
    Create signal for first time login
    https://stackoverflow.com/questions/49385582/can-i-check-if-a-user-is-logged-in-for-the-first-time-after-this-user-is-logged
    More info on signals explained in https://youtu.be/FdVuKt_iuSI?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
    """   
     
    def update_first_login(sender, user, *args, **kwargs):
        if user.last_login is None:
            # First time this user has logged in
            kwargs['request'].session['first_login'] = True #Add first login attribute to session
    # Update the last_login value as normal
        update_last_login(sender, user, **kwargs)

    user_logged_in.disconnect(update_last_login)
    user_logged_in.connect(update_first_login)
   
    
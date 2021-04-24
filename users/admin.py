from django.contrib import admin
from .models import Users
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

"""
Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19

This file defines the properties used in the application Admin page (http://host:port/admin). 
The admin.py file is used to display the user model in the Django admin panel. You can also customize your admin panel by specifying
search_filds, list_filters, list_display and fieldsets. 
Django has a builtin admin interface that reads metadata from the user model, such as fields, and lets you perform CRUD operations against
the model - adduers, delete, modify etc.

"""

class UserAdminConfig(UserAdmin):

    model = Users
    search_fields = ('email', 'user_name', 'first_name', 'last_name',  'phone_number', 'position', 'industry_type__name','city', 'province_state', 'country')
    
    list_filter = ('first_name', 'last_name', 'city', 'province_state', 'country', 'industry_type', 'position', 'is_active', 'is_reviewer')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name', 'last_name', 'phone_number', 'industry_type', 'position', 'company_name',
                'position','website', 'address', 'city', 'province_state', 'country', 'is_active', 'is_reviewer', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'last_name', 'phone_number', 'company_name', 'industry_type', 
                'position','website', 'address', 'city', 'province_state','country', 'last_login', 'start_date')}),
        ('Additional Info', {'fields': ('about',)}),
        ('Permissions', {'fields': ('is_active', 'is_reviewer', 'is_superuser')}),
      
    )
    formfield_overrides = {
        Users.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_reviewer','is_superuser')}
         ),
    )   
admin.site.register(Users,UserAdminConfig)

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Users
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

class UserAdminConfig(UserAdmin):
    model = Users
    search_fields = ('email', 'user_name', 'first_name', 'last_name',  'phone_number', 'industry_type', 'position', 'city', 'province_state', 'country')
    list_filter = ('first_name', 'last_name', 'city', 'province_state', 'country', 'industry_type', 'position', 'is_active', 'is_reviewer', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name', 'last_name', 'phone_number', 'industry_type', 'position', 'company_name', 'industry_type', 
                'position','website', 'address', 'city', 'province_state', 'country', 'is_active', 'is_reviewer', 'is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'last_name', 'phone_number', 'company_name', 'industry_type', 
                'position','website', 'address', 'city', 'province_state','country', 'last_login', 'start_date')}),
        ('Additional Info', {'fields': ('about',)}),
        ('Permissions', {'fields': ('is_active', 'is_reviewer', 'is_staff', 'is_superuser',)}),
      
    )
    formfield_overrides = {
        Users.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_reviewer')}
         ),
    )   
admin.site.register(Users,UserAdminConfig)

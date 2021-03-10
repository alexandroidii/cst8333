from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
#test
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from crispy_forms.bootstrap import FormActions



class LoginForm(forms.Form):

      email = forms.EmailField(required=True)
      password = forms.CharField(widget=forms.PasswordInput())

      class Meta:
            model = get_user_model()
            fields = ['email', 'password']

      def __init__(self, *args, **kwargs):
            super().__init__(*args,**kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
           # self.helper.attrs = { 'novalidate:' '' }
            self.helper.add_input(Submit('login', 'Login', css_class='btn btn-success accept-btn'))
      
      def clean(self, *args,**kwargs):
            query       = self.cleaned_data.get('email')
            password    = self.cleaned_data.get('password')
            user_query  = get_user_model().objects.filter(
                  Q(email__iexact=query)
            ).distinct()

            if not user_query.exists() and user_query !=1:
                 raise forms.ValidationError(_("Invalid credentials - User does not exist"), code='invalid') 
            user_obj = user_query.first()
            if not user_obj.check_password(password):
                  raise forms.ValidationError(_("Password is not correct"), code='invalid') 
            if not user_obj.is_active:
                  raise forms.ValidationError(_("This user is not active"), code='invalid')

            self.cleaned_data["user_obj"] = user_obj
            return super(LoginForm, self).clean(*args,**kwargs)

      
      def clean_email(self):
            email = self.cleaned_data.get('email')

            with open("users/disposable_email_providers.txt",'r') as f:
                  blacklist = f.read().splitlines()

            for disposable_email in blacklist:
                  if disposable_email in email:
                        raise forms.ValidationError(_("Email not allowed using domain: %s" % disposable_email), code='invalid')
            return email


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_name = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
      model = get_user_model() #this is the "AccUser" model that you imported at the top of the file  
      fields = ['email', 'user_name', 'first_name', 'last_name', 'password1', 'password2'] #etc, other fields you want displayed on the form)

            
class ProfileUpdateForm(forms.ModelForm):

      class Meta:
         model = get_user_model() #this is the "Users" model that you imported at the top of the file  
         fields = ('email', 'user_name', 'first_name', 'last_name', 'phone_number','company_name', 'industry_type',
                  'position', 'website', 'address', 'city', 'province_state', 'country') #etc, other fields you want displayed on the form)
   
      widgets = {
          'email': forms.EmailInput(attrs={'class': 'form-control custom-class'}),
          'user_name':forms.TextInput(attrs={'class': 'form-control custom-class'}),
          'first_name':forms.TextInput(attrs={'class': 'form-control custom-class'}),
          'last_name':forms.TextInput(attrs={'class': 'form-control custom-class'}),
          'phone_number':forms.NumberInput(attrs={'class': 'form-control custom-class'}),
          'company_name':forms.TextInput(attrs={'class': 'form-control custom-class'}),
          'position':forms.TextInput(attrs={'class': 'form-control custom-class'}),
          'industry_type':forms.TextInput(attrs={'class': 'form-control custom-class'}),
          'address':forms.TextInput(attrs={'class': 'form-control custom-class'}),
          'city':forms.TextInput(attrs={'class': 'form-control custom-class'}),
          'province_state':forms.TextInput(attrs={'class': 'form-control custom-class'}),
          'country':forms.TextInput(attrs={'class': 'form-control custom-class'}),
            }
      
      def __init__(self, *args, **kwargs):
            super(ProfileUpdateForm, self).__init__(*args, **kwargs)
            self.fields['phone_number'].label = "" #don't display model field - do it in template for this particular case (PhoneField)

            # set which fields are required.
            self.fields['company_name'].required = True
            self.fields['industry_type'].required = True
            self.fields['position'].required = True
            self.fields['country'].required = True

      def __init__(self, *args, **kwargs):
            super().__init__(*args,**kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
           # self.helper.attrs = { 'novalidate:' '' }
            self.helper.add_input(Submit('updateprofile', 'Login', css_class='btn btn-success accept-btn'))

            self.helper.layout = Layout(
                  Row(
                       Column('email'),
                       Column('user_name')     
                  )
            )


      def clean_email(self):
            email = self.cleaned_data.get('email')

            with open("users/disposable_email_providers.txt",'r') as f:
                  blacklist = f.read().splitlines()

            for disposable_email in blacklist:
                  if disposable_email in email:
                        raise forms.ValidationError("Email not allowed using domain: %s" % disposable_email)
            return email



      def clean_first_name(self):
            name = self.cleaned_data['first_name']
            if '@' in name or '-' in name or '|' in name:
                  raise forms.ValidationError("Names should not have special characters.")
            return name

      def clean_last_name(self):
            name = self.cleaned_data['last_name']
            if '@' in name or '-' in name or '|' in name:
                  raise forms.ValidationError("Names should not have special characters.")
            return name
      '''      
      def clean_phone_number(self):
            phone = self.cleaned_data['phone_number']
            print(phone)
            if not phone.isdigit():
                  raise forms.ValidationError('Phone number can only contains digits')
            return phone      
      ''' 
    
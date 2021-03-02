from django import forms
from .models import Users
from django.contrib.auth.forms import UserCreationForm
#test
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from crispy_forms.bootstrap import FormActions


class LoginForm(forms.ModelForm):
 
      class Meta:
            model = Users 
            fields = ['email', 'password']
            
      def __init__(self, *args, **kwargs):
           # super(LoginForm, self).__init__(*args,**kwargs) #needed to do this s button would not show up
            super().__init__(*args,**kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('login', 'Login', css_class='btn btn-success accept-btn'))
            '''
            FormActions(
                  Submit('login', 'Login'),
                  Submit('login', 'Login', css_class='btn btn-success accept-btn')
            )
            '''
      

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    user_name = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
      model = Users #this is the "AccUser" model that you imported at the top of the file  
      fields = ['email', 'user_name', 'first_name', 'last_name', 'password1', 'password2'] #etc, other fields you want displayed on the form)
     

class ProfileUpdateForm(forms.ModelForm):

      class Meta:
         model = Users #this is the "Users" model that you imported at the top of the file  
         
         
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
            self.fields['phone_number'].label = "" #don't display model field - do it in template for this particular case

            # set which fields are required.
            self.fields['company_name'].required = True
            self.fields['industry_type'].required = True
            self.fields['position'].required = True
            self.fields['country'].required = True

      
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
    
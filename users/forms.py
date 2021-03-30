from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.core.validators import RegexValidator 
import re
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column, HTML, Div
from crispy_forms.bootstrap import FormActions, AppendedText
from django.utils.safestring import mark_safe


class NewPassResetForm(forms.ModelForm):
    
    password1 = forms.CharField(label='Enter password',widget=forms.PasswordInput(attrs={'id':'password1'}))
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput(attrs={'id':'password2'}))

    class Meta:
            model = get_user_model() #this is the "AccUser" model that you imported at the top of the file  
            fields = ['password1', 'password2'] #etc, other fields you want displayed on the form)

    def __init__(self, *args, **kwargs):
            super().__init__(*args,**kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-success accept-btn'))
            self.helper.layout = Layout(
                  Row(
                       Column('password1', css_class='col-sm-10 container-fluid  justify-content-center'), 
     
                  ),
                  Row(
                       Column('password2', css_class='col-sm-10 container-fluid  justify-content-center'),  
                         HTML('<my-span class="fa fa-eye" aria-hidden="true" id="eye" onclick="toggle()"</my-span>'),   
                                                        
                                                    
                  ),
             
                       
            )

class MyPasswordResetForm(forms.Form):

      email = forms.EmailField(required=True)

      class Meta:
            model = get_user_model()
            fields = ['email']


      def __init__(self, *args, **kwargs):
            super().__init__(*args,**kwargs)
            self.fields["email"].widget.attrs.update(
                  {"class":"form-control mb-2 email-form", "placeholder":"Email Address"}
            )
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('pw_reset', 'Request Password Reset', css_class='btn btn-success accept-btn'))

      def clean(self, *args,**kwargs):
            query       = self.cleaned_data.get('email')
            user_query  = get_user_model().objects.filter(
                  Q(email__iexact=query)
            ).distinct()
            if not user_query.exists() and user_query !=1:
                 raise forms.ValidationError(_("Invalid account - User does not exist"), code='invalid') 
            user_obj = user_query.first()
            self.cleaned_data["user_obj"] = user_obj
            return super(MyPasswordResetForm, self).clean(*args,**kwargs)
      


class LoginForm(forms.Form):

      email = forms.EmailField(required=True)
      password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'password'}))


      class Meta:
            model = get_user_model()
            fields = ['email', 'password']
      

      def __init__(self, *args, **kwargs):
            super().__init__(*args,**kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('login', 'Login', css_class='btn btn-success accept-btn'))
            self.helper.layout = Layout(
                  Row(
                       Column('email', css_class='col-sm-10 container-fluid  justify-content-center'),    
                  ),
                  Row(

                       Column('password', css_class='col-sm-10 container-fluid  justify-content-center'),  
                         HTML('<my-span class="fa fa-eye" aria-hidden="true" id="eye" onclick="toggle()"</my-span>'),                                                                                                       
                  ),
                  #test
                  # Field('email', css_class='col-sm-10 container-fluid  justify-content-center'),
                  # Field(AppendedText('password',
                  #       mark_safe('<my-span class="fa fa-eye" aria-hidden="true" id="eye" onclick="toggle()"</my-span>'),
                  #       css_class='col-sm-10 container-fluid  justify-content-center')
                  # )                                 
            )

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



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_name = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    password1 = forms.CharField(label='Enter password', 
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', 
                                widget=forms.PasswordInput)

    class Meta:
      model = get_user_model() #this is the "AccUser" model that you imported at the top of the file  
      fields = ['email', 'user_name', 'first_name', 'last_name', 'password1', 'password2'] #etc, other fields you want displayed on the form)
      help_texts = {
            'password1':None,
            'Password2':None,
      }
      
            
class ProfileUpdateForm(forms.ModelForm):

      class Meta:
         model = get_user_model() #this is the "Users" model that you imported at the top of the file  
         fields = ('email', 'user_name', 'first_name', 'last_name', 'phone_number','company_name', 'industry_type',
                  'position', 'website', 'address', 'city', 'province_state', 'country') #etc, other fields you want displayed on the form)
  
      # widgets = {
      #     'email': forms.EmailInput(attrs={'class': 'form-control custom-class'}),
      #     'user_name':forms.TextInput(attrs={'class': 'form-control custom-class'}),
      #     'first_name':forms.TextInput(attrs={'class': 'form-control custom-class'}),
      #     'last_name':forms.TextInput(attrs={'class': 'form-control custom-class'}),
      #     'phone_number':forms.NumberInput(attrs={'class': 'form-control custom-class'}),
      #     'company_name':forms.TextInput(attrs={'class': 'form-control custom-class'}),
      #     'position':forms.TextInput(attrs={'class': 'form-control custom-class'}),
      #     'website':forms.TextInput(attrs={'class': 'form-control custom-class'}),
      #     'industry_type':forms.TextInput(attrs={'class': 'form-control custom-class'}),
      #     'address':forms.TextInput(attrs={'class': 'form-control custom-class'}),
      #     'city':forms.TextInput(attrs={'class': 'form-control custom-class'}),
      #     'province_state':forms.TextInput(attrs={'class': 'form-control custom-class'}),
      #     'country':forms.TextInput(attrs={'class': 'form-control custom-class'}),
      #       }
      
      def __init__(self, *args, **kwargs):
            super(ProfileUpdateForm, self).__init__(*args, **kwargs)        
            # set which fields are disabled and not required
            self.fields['user_name'].widget.attrs['readonly'] = True
            self.fields['user_name'].required = False
            self.fields['first_name'].widget.attrs['readonly'] = True
            self.fields['first_name'].required = False
            # self.fields['last_name'].widget.attrs['readonly'] = True
            # self.fields['last_name'].required = False
            # set which fields are required
            self.fields['company_name']
            self.fields['industry_type'].required = True
            self.fields['position'].required = True
            self.fields['country'].required = True         
            self.fields['phone_number']
            #don't display model field - do it in the helper for this particular case (PhoneField)
            self.fields['phone_number'].label = "" 
            
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('saveprofile', 'Save Profile', css_class='btn btn-success accept-btn'))

            css_class_var = 'col-sm-5 container-fluid  justify-content-center'
            
            self.helper.layout = Layout(
                  Row(
                       Column('email', css_class=css_class_var),  
                       Column('user_name', css_class=css_class_var)       
                  ),
                  Row(
                       Column('first_name', css_class=css_class_var),
                       Column('last_name', css_class=css_class_var)  
                  ),
                  Row(
                        Column('company_name',css_class='col-sm-5 container-fluid ml-4'),
                        Div(
                              Column(
                                    Row(
                                          HTML('<label class="control-label" id="phone_label">Phone number</label>'),
                                    ),
                                    Row(
                                          Div(
                                                'phone_number',css_class='form-inline mr-4',
                                          )
                                    ),
                              ),
                              css_class='form-check'
                        ),
                  ),
                   Row(
                       Column('position',css_class=css_class_var),
                       Column('industry_type',css_class=css_class_var)     
                  ),
                  Row(
                       Column('website',css_class=css_class_var),
                       Column('address',css_class=css_class_var)    
                  ),
      
                  Row(
                       Column('city',css_class=css_class_var),
                       Column('province_state',css_class=css_class_var)     
                  ),
                  Row(
                       Column('country',css_class='col-sm-5 container-fluid  ml-4'),  
                       Column(css_class='col-sm-6 container-fluid  justify-content-center'), 
                   )
            )

      # def clean_phone_number(self):
      #       phone_number = self.cleaned_data.get('phone_number', None)
      #       try:
      #             int(phone_number)
      #       except (ValueError, TypeError):
      #             raise forms.ValidationError('Please enter a valid phone number')
      #       return phone_number


      
      def clean_email(self):
            email = self.cleaned_data.get('email')

            with open("cst8333/users/disposable_email_providers.txt",'r') as f:
                  blacklist = f.read().splitlines()

            for disposable_email in blacklist:
                  if disposable_email in email:
                        raise forms.ValidationError(_("Email not allowed using domain: %s" % disposable_email), code='invalid')
            return email
            

      def clean_last_name(self):
            name = self.cleaned_data.get("last_name")
            if '@' in name or '-' in name or '|' in name:
                  raise forms.ValidationError("Names should not have special characters.")
            return name

            
      # def clean_phone_number(self):
      #       phone = self.cleaned_data.get("phone_number")
      #       phone_req = "6137624063"
      #       #print(phone)
      #       #if not(str(phone).isalpha()):
      #       # if phone_req != phone:
      #       #      # print(phone)
      #       #       raise forms.ValidationError("Phone number doesn't match")
      #       if not re.sub("['^\+?1?\d{9,15}$']", " ", str(phone)):
      #             raise forms.ValidationError("Only numbers accepted")
      #       return phone     
       
    
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import UserRegisterForm,ProfileUpdateForm,LoginForm,MyPasswordResetForm,NewPassResetForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, BadHeaderError
from .utils import token_generator
from django.http import HttpResponse
from .models import Users as User
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
import threading
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.views.generic.edit import FormView
from rlcs.decorator import already_authenticated_user


"""
CCS Views that handle all users information contained in Db model
with a custom user model authentication framework. Summarization list below:

Functions and classes:
EmailThread -- Email sending threading (Class)
register -- Provides user registration process (Function)
RequestPasswordResetEmail - Provision for user passwored reset (Class) 
VerificationView - Handles verification of newly registered user (Class)
CompletePasswordReset - Validates user on password reset (Class)
profile - Provides access to personal profile (Function)
landing - Simple function for redirecting to the CCS application home page (Function)
LoginView - Provide login credential checking, authentication and redirection to index - landing page (Class)
LogoutView - Calls logout within Djano to log user out (Class)

Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19
"""

"""
Due to the synchronous nature of the default Django email process due to Djano handling both the view and email
simultaneously, this proved unacceptable for a positive user experience. By implementing threading of the email process to
provide aynchronous operation of email within it's own thread, immediate processing takes place since it's within it's own thread
which ultamatly speeds up email sending. 
https://youtu.be/7oruVMyE3J0
"""
class EmailThread(threading.Thread):
     
    def __init__(self, email_message):
        self.email_message=email_message
        threading.Thread.__init__(self)

#define run method
    def run(self):
        self.email_message.send()
    
"""
Forms/templates: UserRegisterForm, send_acc_activate.html
Methods: GET/POST
Other: Google reCAPTCHA
Output: Successful registration banner message upon conclusion of submission.
Output other: Email sent to new user

The register Function handles both the GET and POST registration activity while rendering the registration form.
The new user would fill out the form fields which include email address as the primary key for the user
within the custom Users model, a User Name, First name, Last name, password1, password2 as wel as a call to implement
Google's reCAPTCHA to prevent robot like entries. Only when reCAPTCHA has completed verification, the submission is accepted.
Most of the form is generated using a form class in forms.py with the particular class being UserRegisterForm.
The register function will also check the Users model to see if the user already exists. If so, the user is notified. However, while 
the new user is added, they are done so in an inactive state and only when verified, the account is activated. 
Once a new user has been accepted, an activation process is initiated which then sends an email link appened with a security token
to the new user. The link along with the token generated by the PasswordResetTokenGenerator class with base64 encoding facilitates 
the use of send_acc_activate.html template where the message is rendered along with the token, then sent asynchronously via the email threading
mechanism to the new user via the EmailThread mechanism. The sites framework provides the domain information - configurable via sites properties 
in the admin page.

Used combination of documentation and Youtube
https://docs.djangoproject.com/en/3.1/topics/auth/customizing/
    
"""
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            email_address = form.cleaned_data.get('email').lower()
             # Check to see if any users already exist with this email as a username.
            if User.objects.filter(email=email_address).exists():
                messages.error(request, 'This email address is already in use.e')
                return render(request, 'users/register.html', {'form': form, 'activePage': 'register'})
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            message = render_to_string('users/send_acc_activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token_generator.make_token(user),
            })           
            email = EmailMessage(email_subject, message, to=[email_address])
            EmailThread(email).start()
            messages.success(request, f'Account created for {user}. Check your inbox to activate')
            #return redirect ('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'activePage': 'register'})



"""
Forms/templates: MyPasswordResetForm, password_reset.html
Methods: GET/POST
Output: Successful banner message upon conclusion of reset request.
Output other: Email sent to existing user

The RequestPasswordResetEmail class makes use of similar processes of tokenizing and templates as that of the register function process
for the password reset functionality. Most of the form is generated using a form class in forms.py - MyPasswordResetForm. Some html decoration 
is added in the password_reset.html template. However, this is mainly styling.
Upon request for a password reset, the reset process is initiated only when verified as a current registered user
which then sends an email link appened with a security token. The link along with the token generated by the PasswordResetTokenGenerator class 
with base64 encoding facilitates the use of password_reset.html template where the message is rendered along with the token, then sent asynchronously via the email threading
to the user via the EmailThread mechanism. The sites framework provides the domain information - configurable via sites properties 
in the admin page.

https://www.ordinarycoders.com/blog/article/django-password-reset
https://www.youtube.com/watch?v=a2Rom1nfHRs

"""
class RequestPasswordResetEmail(View):
    form = MyPasswordResetForm
    template_name = 'users/password_reset.html'
    
    def get(self, request):
        form = self.form(None)
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        form = self.form(request.POST)
        email_address = request.POST['email'].lower()

        context = {
            'values':request.POST
        }
        email_template_name = "users/password_reset.html"

        current_site = get_current_site(request)
 
        user = User.objects.filter(email=email_address)

        if user.exists():
                message = render_to_string('users/send_acc_reset.html', {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
                })

                email_subject = 'Password Reset Your Account'
                email = EmailMessage(email_subject, message, to=[email_address])
                EmailThread(email).start()
                messages.success(request, 'We have sent you an email to reset your password')  
                
                return render(request, self.template_name, {'form': form})   

        else:
            return render(request, "users/password_reset.html",{'form': form})   

"""
Forms/templates: N/A
Methods: GET
Inputs: <uidb64>/<token>
Output: Successful banner message for account activation completion.

This class is called through the url mapping which also passes via the url, the encoded uid base 64 token. The user is retrived from the model 
after the token is decoded and checked (via primary key). If the current user is not activated - as it should be for a new user, the is_active 
boolean is set in the users model which then via the Django authentication mechanism, enables the user to log into the application while being
routed via the login screen. A banner message appears between the login template and the banner for 3 seconds notifying to the user that
the account was activated. The sites framework provides the domain information - configurable via sites properties 
in the admin page.

"""

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('users:login')
            user.is_active = True
            user.save()
          
            messages.success(request, 'Your account has been activated successfully')
            return redirect('users:login')

        except Exception as ex:
            pass

        return redirect('users:login')


"""
https://youtu.be/a2Rom1nfHRs
https://simpleisbetterthancomplex.com/tutorial/2016/08/24/how-to-create-one-time-link.html

"""
class CompletePasswordReset(View):
    form = NewPassResetForm
    template_name = 'users/set-new-password.html'

    def get(self, request, uidb64, token):
        form = self.form(None)

        context = {
            'uidb64':uidb64,
            'token': token,
            'form': form
        }
        # check to see if user uses the link a second time and invalidate if true
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)
        """
        Can't seem to get this to work. PasswordResetTokenGenerator always
        returns false.Tried to add more field in utils, no change
        """
        try:        
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.error(request, 'Password link is invalid, please request a new one')
                return redirect ('users:login')
        except Exception as identifier:
                #import pdb #setup debugger so you can see what identifier is
                #pdb.set_trace()
                pass
        return render(request,'users/set-new-password.html',context)


    def post(self, request, uidb64, token):
        form = self.form(None)
        context = {
            'uidb64':uidb64,
            'token': token,
            'form': form
        }
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request,'users/set-new-password.html', context)

        if len(password1) < 6:
            messages.error(request, 'Password too short')
            return render(request,'users/set-new-password.html', context)

        try:
            id = force_bytes(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=id)
            user.set_password(password1)
            user.save()

            messages.success(request, 'Password reset successfully, you may login with your new password')
            return redirect ('users:login')

        except Exception as identifier:
          #  import pdb #setup debugger so you can see what identifier is
          #  pdb.set_trace()
            messages.error(request, 'Something went wrong, try again')
            return render(request,'users/set-new-password.html', context)

            

@login_required #login required decorator
def profile(request):
    if request.method == 'POST':
        #print(request.POST)
        form = ProfileUpdateForm(request.POST,instance=request.user)
        if  form.is_valid():
            form.save()
            messages.success(request, f'You profile has been updated')
            form = ProfileUpdateForm() #clear form after submit
            return redirect ('users:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {
        'form':form,
        'activePage': 'profile'
    }
    return render(request, 'users/profile.html', context)


"""
Check if logging in the first time
https://stackoverflow.com/questions/49385582/can-i-check-if-a-user-is-logged-in-for-the-first-time-after-this-user-is-logged
"""
def landing(request):
    context={}
    if request.user:
        if request.session.get('first_login'):
            return redirect('users:profile')
        else:
            #return render(request, 'rlcs/landing.html', {'activePage': 'home'})
            return redirect('rlcs:home')
    else:
        return redirect('users:login')

class LoginView(View):
    form = LoginForm
    template_name = 'users/login.html'
    
    def get(self, request):
        form = self.form(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user = None
        form = self.form(request.POST)
        
        try:
            referer = request.session['referer_link']
            
            # This is because when you are going to the login link directly, there is no request.path_info
            if referer == None:
                referer = '/'
        except:
            referer = '/'

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
        #check with cst8333.backends.CustomEmailAuthBackend.CaseInsensitiveAuth
            user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(referer)

        return render(request, self.template_name, {'form': form})
    
class LogoutView(View):
    template_name = 'users/logout.html'
   
    def get(self, request):
        logout(request)
        return render(request, self.template_name)


from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import UserRegisterForm,ProfileUpdateForm,LoginForm
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
import threading
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
#test
from django.views.generic import FormView


"""
Speed up email sending
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
    Used combination of documentation and Youtube
    https://docs.djangoproject.com/en/3.1/topics/auth/customizing/


    """
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
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
            email_address = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[email_address])
            EmailThread(email).start()
            messages.success(request, f'Account created for {user} with email address {email_address}! Check your inbox to activate')
            return redirect ('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'activePage': 'register'})



"""
https://www.ordinarycoders.com/blog/article/django-password-reset
https://www.youtube.com/watch?v=a2Rom1nfHRs

"""
class RequestPasswordResetEmail(View):
    def get(self,request):
        return render(request,'users/password_reset.html')

    def post(self,request):
        email_address = request.POST['email']

        context = {
            'values':request.POST
        }
        email_template_name = "users/password_reset.html"

        
       # if  validate_email(email_address):
           # messages.error(request, 'Please supply a valid email')
           # return render(request,'users/password_reset.html', context)

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
           
        return render(request,'users/password_reset.html')



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
    def get(self, request, uidb64, token):

        context = {
            'uidb64':uidb64,
            'token': token
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
                messages.info(request, 'Password link is invalid, please request a new one')
                return redirect ('users:login')
        except Exception as identifier:
                #import pdb #setup debugger so you can see what identifier is
                #pdb.set_trace()
                pass
        return render(request,'users/set-new-password.html',context)


    def post(self, request, uidb64, token):

        context = {
            'uidb64':uidb64,
            'token': token
        }
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.warning(request, 'Passwords do not match')
            return render(request,'users/set-new-password.html', context)

        if len(password) < 6:
            messages.warning(request, 'Password too short')
            return render(request,'users/set-new-password.html', context)

        try:
            id = force_bytes(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=id)
            user.set_password(password)
            user.save()

            messages.success(request, 'Password reset successfully, you may login with your new password')
            return redirect ('users:login')

        except Exception as identifier:
          #  import pdb #setup debugger so you can see what identifier is
          #  pdb.set_trace()
            messages.info(request, 'Something went wrong, try again')
            return render(request,'users/set-new-password.html', context)

            

@login_required #login required decorator
def profile(request):
    if request.method == 'POST':
        #print(request.POST)
        u_form = ProfileUpdateForm(request.POST,instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Profile has been updated')
            u_form = ProfileUpdateForm() #clear form after submit
            return redirect ('users:profile')
        ''' 
        else:
            messages.warning(request, ('ERROR: Compile the form properly! '))
            print(u_form.errors)
            return redirect ('users:profile')
        '''
    else:
        u_form = ProfileUpdateForm(instance=request.user)

    context = {
        'u_form':u_form,
        'activePage': 'profile'
    }
    return render(request, 'users/profile.html', context)


"""
Check if logging in the first time
https://stackoverflow.com/questions/49385582/can-i-check-if-a-user-is-logged-in-for-the-first-time-after-this-user-is-logged
"""
def index(request):
    context={}
    if request.user:
        if request.session.get('first_login'):
          #  return render(request, 'users/profile.html', context)
            return redirect('users:profile')
        else:
            return render(request, 'rlcis/index.html', {'activePage': 'home'})
    else:
        return redirect('users:login')

    ''' 
class LoginView(FormView):
    form = LoginForm
    success_url = '/'
    template_name = 'users/login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=email, passord=password)
        if user is not None:
            login(request, user)
            try:
                pass
            except:
                pass
            if is_safe_url(redirect_path. request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
 
        return super(LoginPage, self).form_invalid()
    '''
    '''
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=email, password=password)

        # Check here if the user is an admin
        if user is not None and user.is_active and user.is_staff:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(form)
   
    '''
'''  
def loginView(request):

    from django.conf import settings
    print(settings.AUTHENTICATION_BACKENDS)
    form = LoginForm()
       
    if request.method == 'POST':
        print(request.POST)
        form = LoginForm()
        
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=username, passord=password)
            
        if user is not None:
            login(request, user)
            redirect('home')
        else:
            form = LoginForm()

    else:
        context={
       'form': form,
       'activePage': 'login'
            }
      
    return render(request, 'users/login.html', {'form': form})
'''       
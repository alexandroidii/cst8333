
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import resolve

def already_authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        try:
            if request.user:
                if request.user.is_authenticated:
                    return view_func(request, *args, **kwargs)
                else:
                    request.session['referer_link'] = request.path_info
                    return redirect('users:login')
        except:
            # request.session['referer_link'] = request.path_info
            return redirect('users:login')
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator


# def reviewer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
#     '''
#     Decorator for views that checks that the logged in user is a student,
#     redirects to the log-in page if necessary.
#     '''
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and u.is_reviewer,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator

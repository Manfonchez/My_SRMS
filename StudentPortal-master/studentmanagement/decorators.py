from django.http import HttpResponse
from django.shortcuts import redirect


# This decorator is called when the user is NOT authenticated hence redirected to login & register pages
def unauthenticated_user(view_func):
    # Wrapper function
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

# This decorator will allow users of a certain Role to access the specified webpages
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return (HttpResponse('You are not authorized to view this page'))

        return wrapper_func
    return decorator


# This decorator is for the Dashboard and pages that the 'Admin alone' should access
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'student':
            return redirect('student_page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)
            
    return wrapper_func
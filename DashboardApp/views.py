from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, WallPost, Comment
import bcrypt

# GET GET GET GET GET GET GET

def display_home(request):
    context = {
        'page_title': 'Welcome To Our Test Page!'
    }
    return render(request, 'html/home.html', context)

def display_login(request):
    context = {
        'page_title': 'Sign In Here!'
    }
    return render(request, 'html/sign_in.html', context)

def display_register(request):
    context = {
        'page_title': 'Register For An Account!'
    }
    return render(request, 'html/register.html', context)

def display_user_dashboard(request):
    context = {
        'users': User.objects.all(),
        'current_user': User.objects.get(id = request.session['userid'])
    }
    return render(request, 'html/user_dashboard.html', context)


# POST POST POST POST POST POST POST

def handle_registration(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='danger')
            return redirect('login')
        prehash = request.POST['register-password']
        hashedPW = bcrypt.hashpw(prehash.encode(), bcrypt.gensalt()).decode()
        if not User.objects.filter(id = 1):
            userlvl = 9
        else:
            userlvl = 1
        newuser = User.objects.create(
            email = request.POST['register-email'],
            first_name = request.POST['register-first-name'],
            last_name = request.POST['register-last-name'],
            password = hashedPW,
            user_level = userlvl
        )
        print(f'DEBUG - ID = {newuser.id}, LEVEL = {newuser.user_level}, email = {newuser.email}')
        request.session['userid'] = newuser.id
        request.session['userlevel'] = newuser.user_level
        request.session['username'] = newuser.first_name
        messages.success(request, f"{ newuser.first_name }, an account with the email { newuser.email } has been created successfully!")
        return redirect('dashboard')

def handle_login(request):
    pass
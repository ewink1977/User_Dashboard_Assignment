from django.shortcuts import render, redirect, HttpResponse
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

def logoff(request):
    del request.session['userid']
    del request.session['userlevel']
    del request.session['username']
    return redirect('home')

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

def display_admin_dashboard(request):
    context = {
        'users': User.objects.all(),
        'current_user': User.objects.get(id = request.session['userid'])
    }
    return render(request, 'html/admin_dashboard.html', context)

def show_user_profile(request):
    pass

def edit_user_profile(request, userid):
    pass

def show_user_wall(request, userid):
    pass

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
    if request.method == 'POST':
        logging_in_user = User.objects.filter(email = request.POST['email-signin'])
        if logging_in_user:
            user = logging_in_user[0]
            if bcrypt.checkpw(
                request.POST['password-signin'].encode(),
                user.password.encode()
            ):
                request.session['userid'] = user.id
                request.session['userlevel'] = user.user_level
                request.session['username'] = user.first_name
                messages.success(request, f"{ user.email } has successfully logged in!")
                return redirect('dashboard')
            else:
                messages.error(request, 'Unable to log in. The password you entered is incorrect.', extra_tags = 'danger')
                return redirect('login')
        else:
            messages.error(request, "That email was not found in our database. Please retry or register for a new account!", extra_tags = 'danger')
            return redirect('login')
    else:
        messages.error(request, "Invalid request.", extra_tags = 'danger')
        return redirect('login')

def delete_user(request, userid):
    return HttpResponse(f'If this page was complete, user number {userid} would have been deleted!')
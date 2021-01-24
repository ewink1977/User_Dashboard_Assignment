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
        'current_user': User.objects.get(id = request.session['userid']),
        'page_title': 'User Dasboard!'
    }
    return render(request, 'html/user_dashboard.html', context)

def display_admin_dashboard(request):
    if not request.session['userlevel'] == 9:
        messages.error(request, 'Sorry, you must be an administrator to access this page.', extra_tags = 'danger')
        return redirect('dashboard')
    context = {
        'users': User.objects.all(),
        'current_user': User.objects.get(id = request.session['userid']),
        'page_title': 'Admin Dashboard'
    }
    return render(request, 'html/admin_dashboard.html', context)

def show_add_user(request):
    if not request.session['userlevel'] == 9:
        messages.error(request, 'Sorry, you must be an administrator to access this page.', extra_tags = 'danger')
        return redirect('dashboard')
    context = {
        'page_title': f'Add a User'
    }
    return render(request, 'html/add_user.html', context)

# Function for admin editing of users.
def edit_user_profile(request, userid):
    if not request.session['userlevel'] == 9:
        messages.error(request, 'Sorry, you must be an administrator to access this page.', extra_tags = 'danger')
        return redirect('dashboard')
    context = {
        'user': User.objects.get(id = userid),
        'page_title': f'Edit User ID #{userid}'
    }
    return render(request, 'html/edit_user.html', context)

# Function for user editing of their own profile. 
def show_user_profile(request, userid):
    context = {
        'user': User.objects.get(id = userid),
        'page_title': 'User Profile!'
    }
    return render(request, 'html/self_profile.html', context)


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

def handle_add_user(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='danger')
            return redirect('login')
        prehash = request.POST['register-password']
        hashedPW = bcrypt.hashpw(prehash.encode(), bcrypt.gensalt()).decode()
        newuser = User.objects.create(
            email = request.POST['register-email'],
            first_name = request.POST['register-first-name'],
            last_name = request.POST['register-last-name'],
            password = hashedPW,
            user_level = 1
        )
        messages.success(request, f"{ newuser.email } has been successfully created!")
        return redirect('admin_dashboard')

def delete_user(request, userid):
    if request.method == 'POST':
        user_to_destroy = User.objects.get(id = userid)
        user_to_destroy.delete()
        messages.success(request, f"{ user_to_destroy.email } has been successfully deleted!")
        return redirect('admin_dashboard')
    else:
        messages.error(request, "Invalid request.", extra_tags = 'danger')
        return redirect('dashboard')

def process_edit_user_profile(request, userid):
    if request.method == 'POST':
        user_to_update = User.objects.get(id = userid)
        user_to_update.email = request.POST['email']
        user_to_update.first_name = request.POST['first-name']
        user_to_update.last_name = request.POST['last-name']
        user_to_update.user_level = request.POST['user-level']
        user_to_update.save()
        messages.success(request, f"User { user_to_update.email } has been successfully updated!")
        return redirect('edit_user_profile', userid)
    else:
        messages.error(request, "Invalid request.", extra_tags = 'danger')
        return redirect('dashboard')

def process_self_edit_profile(request, userid):
    if request.method == 'POST':
        user_to_update = User.objects.get(id = userid)
        user_to_update.email = request.POST['email']
        user_to_update.first_name = request.POST['first-name']
        user_to_update.last_name = request.POST['last-name']
        messages.success(request, f"User { user_to_update.email } has been successfully updated!")
        return redirect('user_profile', userid)
    else:
        messages.error(request, "Invalid request.", extra_tags = 'danger')
        return redirect('dashboard')

def process_edit_user_password(request, userid):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='danger')
            return redirect('login')
        prehash = request.POST['password']
        hashedPW = bcrypt.hashpw(prehash.encode(), bcrypt.gensalt()).decode()
        user_to_update = User.objects.get(id = userid)
        user_to_update.password = hashedPW
        messages.success(request, f"The password for { user_to_update.email } has been successfully updated!")
        return redirect('edit_user_profile', userid)
    else:
        messages.error(request, "Invalid request.", extra_tags = 'danger')
        return redirect('dashboard')

def process_self_edit_password(request, userid):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='danger')
            return redirect('login')
        prehash = request.POST['password']
        hashedPW = bcrypt.hashpw(prehash.encode(), bcrypt.gensalt()).decode()
        user_to_update = User.objects.get(id = userid)
        user_to_update.password = hashedPW
        messages.success(request, f"The password for { user_to_update.email } has been successfully updated!")
        return redirect('user_profile', userid)
    else:
        messages.error(request, "Invalid request.", extra_tags = 'danger')
        return redirect('dashboard')

def process_self_edit_description(request, userid):
    if request.method == 'POST':
        user_to_update = User.objects.get(id = userid)
        user_to_update.description = request.POST['description']
        user_to_update.save()
        messages.success(request, f"The description for { user_to_update.email } has been successfully updated!")
        return redirect('user_profile', userid)
    else:
        messages.error(request, "Invalid request.", extra_tags = 'danger')
        return redirect('dashboard')
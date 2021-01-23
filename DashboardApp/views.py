from django.shortcuts import render, redirect

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


# POST POST POST POST POST POST POST
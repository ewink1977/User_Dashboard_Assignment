from django.shortcuts import render, redirect

def display_home(request):
    return render(request, 'html/home.html')


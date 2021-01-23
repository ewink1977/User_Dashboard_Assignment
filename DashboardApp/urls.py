from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_home, name = 'home'),
    path('signin', views.display_login, name = 'login'),
    path('register', views.display_register, name = 'register'),
    path('handle-reg', views.handle_registration, name = 'handle-reg'),
    path('dashboard', views.display_user_dashboard, name = 'dashboard')
]


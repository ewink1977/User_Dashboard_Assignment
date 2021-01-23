from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_home, name = 'home'),
    path('signin', views.display_login, name = 'login'),
    path('handle-signin', views.handle_login, name = 'handle-signin'),
    path('logoff', views.logoff, name = 'logoff'),
    path('register', views.display_register, name = 'register'),
    path('handle-reg', views.handle_registration, name = 'handle-reg'),
    path('dashboard', views.display_user_dashboard, name = 'dashboard'),
    path('dashboard/admin', views.display_admin_dashboard, name = 'admin_dashboard'),
    path('users/edit', views.show_user_profile, name = 'user_profile'),
    path('users/edit/<int:userid>', views.edit_user_profile, name = 'edit_user_profile'),
    path('users/delete/<int:userid>', views.delete_user, name = 'delete_user'),
    path('users/show/<int:userid>', views.show_user_wall, name = 'show_user_wall'),
]


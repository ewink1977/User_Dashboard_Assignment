from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_home, name = 'home'),
    # Sign In and Registration
    path('signin', views.display_login, name = 'login'),
    path('handle-signin', views.handle_login, name = 'handle-signin'),
    path('logoff', views.logoff, name = 'logoff'),
    path('register', views.display_register, name = 'register'),
    path('handle-reg', views.handle_registration, name = 'handle-reg'),
    # Dashboards
    path('dashboard', views.display_user_dashboard, name = 'dashboard'),
    path('dashboard/admin', views.display_admin_dashboard, name = 'admin_dashboard'),
    # User Editing
    path('users/<int:userid>/edit', views.show_user_profile, name = 'user_profile'),
    path('users/<int:userid>/edit/process/user', views.process_self_edit_profile, name = 'self_edit_profile'),
    path('users/<int:userid>/edit/process/pw', views.process_self_edit_password, name = 'self_edit_password'),
    path('users/<int:userid>/edit/process/desc', views.process_self_edit_description, name = 'self_edit_description'),
    # Admin Editing
    path('users/edit/<int:userid>', views.edit_user_profile, name = 'edit_user_profile'),
    path('users/edit/<int:userid>/process/info', views.process_edit_user_profile, name = 'process_edit_user_profile'),
    path('users/edit/<int:userid>/process/pw', views.process_edit_user_password, name = 'process_edit_user_password'),
    path('users/delete/<int:userid>', views.delete_user, name = 'delete_user'),
    path('users/new', views.show_add_user, name = 'add_new_user'),
    path('users/new/process', views.handle_add_user, name = 'handle_new_user'),
    # Wall Posts And Comments
    path('users/show/<int:userid>', views.show_user_wall, name = 'show_user_wall'),
    path('users/show/<int:userid>/post2wall', views.process_WallPost, name = 'post_to_wall'),
    path('users/show/<int:userid>/comment', views.process_CommentAdd, name = 'post_comment'),
]


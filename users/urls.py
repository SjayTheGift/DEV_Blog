from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, ProfileView
from django.shortcuts import redirect

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', success_url='profile'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('password_reset/', 
        auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), 
        name='password_reset'),
        
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    path('password/',  
    auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html',
       success_url ='password'
      
    ), name='password')
]

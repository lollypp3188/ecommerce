from django.urls import path
from . import views


urlpatterns = [
  path('register', views.register, name='register'),
  path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email-verification'),
  path('email-verification-sent', views.email_verification_sent, name='email-verification-sent'),
  path('email-verification-success', views.email_verification_success, name='email-verification-success'),
  path('email-verification-failed', views.email_verification_failed, name='email-verification-failed'),
  path('login-account', views.login_account, name='login-account'),
  path('dashboard', views.dashboard, name='dashboard'),
  path('logout-user', views.logout_user, name='logout-user'),
  path('profile-management', views.profile_management, name='profile-management'),
  path('delete-account', views.delete_account, name='delete-account'),
]

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, email_verification, RestorePassword

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('company/', ProfileView.as_view(), name='profile'),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path('restore-password/', RestorePassword.as_view(), name='restore-password')
]
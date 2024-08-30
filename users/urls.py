from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import StyledLoginView, RegisterView, ProfileView, email_verification, password_recovery, UsersView

app_name = UsersConfig.name

urlpatterns = [
    path('', StyledLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users_update/<int:pk>', ProfileView.as_view(), name='profile'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('password_recovery/', password_recovery, name='new_password'),
    path('users_account/', UsersView.as_view(), name='users_account'),
]


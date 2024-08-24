from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from dentistry.views import IndexView
from users.views import StyledLoginView

app_name = UsersConfig.name

urlpatterns = [
    path('', StyledLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

from django.contrib.auth.views import LoginView
from users.forms import StyledFormMixin


class StyledLoginView(StyledFormMixin, LoginView):
    template_name = 'users/login.html'

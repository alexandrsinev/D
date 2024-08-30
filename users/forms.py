from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm

from dentistry.forms import StileFormMixin
from users.models import Users


class UserRegisterForm(StileFormMixin, UserCreationForm):
    class Meta:
        model = Users
        fields = ('email', 'password1', 'password2')


class UserProfileForm(StileFormMixin, forms.ModelForm):
    class Meta:
        model = Users
        fields = ('email', 'first_name', 'last_name', 'phone', )




class StyledFormMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['username'].widget.attrs.update({'class': 'form-control'})
        form.fields['password'].widget.attrs.update({'class': 'form-control'})
        return form

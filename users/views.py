import secrets

from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
import random

from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from appointment.models import Appointment
from users.forms import StyledFormMixin

from users.forms import UserRegisterForm, UserProfileForm
from users.models import Users
from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    model = Users
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Перейдите по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        messages.success(self.request, 'Ссылка для подтверждения почты отправлена на ваш email.')
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(Users, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileView(UpdateView):
    model = Users
    form_class = UserProfileForm
    success_url = reverse_lazy('users:users_account')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


def password_recovery(request):
    context = {
        'success_message': 'Пароль успешно сброшен. Новый пароль был отправлен на ваш адрес электронной почты.',
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(Users, email=email)
        a = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        b = 'abcdefghijklmnopqrstuvwxyz'
        c = '0123456789'
        length = 8
        all = a + b + c
        password = "".join(random.sample(all, length))
        user.set_password(password)
        user.save()
        send_mail(
            subject='Восстановление пароля',
            message=f'Ваш новый пароль: {password}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return render(request, 'users/password_recovery.html', context)
    else:
        return render(request, 'users/password_recovery.html')


class StyledLoginView(StyledFormMixin, LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:users_account')

    def form_valid(self, form):
        response = super().form_valid(form)

        moderator_group = Group.objects.get(name='Moderator')
        if moderator_group in self.request.user.groups.all():
            return redirect(reverse('dentistry:base'))
        else:
            return response

    def get_success_url(self):
        return self.success_url


class UsersView(View):
    model = Users

    def get(self, request):
        user = request.user
        appointments = Appointment.objects.filter(user=user)
        if user.is_authenticated:
            return render(request, 'users/users_account.html', {'user': user, 'appointments': appointments})
        else:
            return redirect('users:login')



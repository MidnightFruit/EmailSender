import secrets
import string
import random

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.forms import RegisterForm, UserProfileForm
from users.models import User

from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('company:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        host = self.request.get_host()
        user.token = token
        user.save()
        url = f'http://{host}/email-confirm/{token}'

        send_mail(subject='Подтверждение регистрации', message="Здравствуйте, Вы регистрируетесь в системе рассылки\n"
                                                               f"Ссылка для подтверждения регистрации {url}",
                  from_email=EMAIL_HOST_USER, recipient_list=[user.email])
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("company:login"))


class RestorePassword(PasswordResetView):
    form_class = PasswordResetForm
    template_name = "users/restore_password.html"
    success_url = reverse_lazy("company:login")

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        if user:
            characters = string.ascii_letters + string.digits + string.punctuation
            new_password = ''.join(random.choice(characters) for _ in range(12))
            send_mail(subject="Восстановление пароля", message=f"Здравствуйте!!\n"
                                                               f" Ваш новый пароль для входа: {new_password}",
                      from_email=EMAIL_HOST_USER, recipient_list=[user.email])
            user.set_password(new_password)
            user.save()
            return redirect(reverse('company:login'))
        else:
            return redirect(reverse('company:restore-password'))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('company:profile')

    def get_object(self, queryset=None):
        return self.request.user

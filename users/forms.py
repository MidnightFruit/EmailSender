from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import Company


class RegisterForm(UserCreationForm):
    class Meta:
        model = Company

        fields = ('email', 'password1', 'password2', 'country', 'phone', 'company_name')


class UserProfileForm(UserChangeForm):
    class Meta:
        model = Company
        fields = ('email', 'password', 'country', 'phone', 'company_name')

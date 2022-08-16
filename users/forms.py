from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = ['image',]
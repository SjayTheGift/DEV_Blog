from cProfile import label
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

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

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)

        for fieldname in ['password',]:
            self.fields[fieldname].help_text = None


class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = ['image',]
    
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)

        for fieldname in ['password',]:
            self.fields[fieldname].disabled = True
            self.fields[fieldname].help_text = None
            


class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']


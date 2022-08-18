from urllib import request
from django.shortcuts import redirect, render
from django.views.generic import CreateView, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



class RegisterView(CreateView):

    def get(self, request, *args, **kwargs):
        context = {'form': CustomUserCreationForm()}
        return render(request, 'users/register.html', context)

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account has been created successfullly')
            return redirect('login')
        return render(request, 'users/register.html', {'form': form})


class ProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'users/profile.html', context)

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        return render(request, 'users/profile.html', context)


class PasswordChangeView(LoginRequiredMixin, View):
    template_name = 'users/password_change.html'

    def get(self, request, *args, **kwargs):
        context = {'form': PasswordChangeForm(request.user)}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        context = {'form': form}
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was changed successfully!')
            return redirect('profile')
        return render(request, self.template_name, context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserUpdateForm

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('¡Registro completado! Bienvenido/a.'))
            return redirect('users:profile')
        else:
            messages.error(request, _('Por favor corrige los errores del formulario.'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:profile')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, _('Has iniciado sesión correctamente.'))
            next_url = request.GET.get('next')
            return redirect(next_url or 'users:profile')
        else:
            messages.error(request, _('Credenciales inválidas.'))
    else:
        form = CustomAuthenticationForm(request)
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, _('Has cerrado sesión.'))
    return redirect('users:login')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user_obj': request.user})


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Perfil actualizado correctamente.'))
            return redirect('users:profile')
        else:
            messages.error(request, _('Revisa los errores del formulario.'))
    else:
        form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


def public_profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    return render(request, 'users/public_profile.html', {'user_obj': user_obj})

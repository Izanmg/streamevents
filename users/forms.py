
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
import re

User = get_user_model()

USERNAME_REGEX = re.compile(r'^[\w.@+-]+$')

class CustomUserCreationForm(forms.ModelForm):
    """Registro de nuevos usuarios con validaciones de email único y password fuerte."""
    password1 = forms.CharField(
        label=_('Contraseña'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Contraseña')}),
        strip=False,
        help_text=_('Usa una contraseña segura.')
    )
    password2 = forms.CharField(
        label=_('Confirmar contraseña'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Repite la contraseña')}),
        strip=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Usuario')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nombre')}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Apellidos')}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not USERNAME_REGEX.match(username):
            raise ValidationError(_('El usuario solo puede contener letras, números y @/./+/-/_ .'))
        return username

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(_('Ya existe un usuario con ese email.'))
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', _('Las contraseñas no coinciden.'))
        # Validación de complejidad usando los validadores configurados en settings.AUTH_PASSWORD_VALIDATORS
        if p1:
            try:
                validate_password(p1, user=None)
            except ValidationError as e:
                self.add_error('password1', e)
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomUserUpdateForm(forms.ModelForm):
    """Edición de perfil del usuario actual."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'display_name', 'bio', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nombre')}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Apellidos')}),
            'display_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nombre público')}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Cuéntanos algo sobre ti...')}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    """Permite login con username o email manteniendo la lógica estándar de Django."""
    username = forms.CharField(
        label=_('Usuario o email'),
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': _('Usuario o email')})
    )
    password = forms.CharField(
        label=_('Contraseña'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Contraseña')}),
    )

    error_messages = {
        "invalid_login": _(
            "Por favor, introduce un usuario/email y contraseña correctos. "
            "Ten en cuenta que ambos campos pueden ser sensibles a mayúsculas."
        ),
        "inactive": _("Esta cuenta está inactiva."),
    }

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username_or_email and password:
            # Si parece un email, intentamos resolver al username real
            resolved_username = username_or_email
            if '@' in username_or_email:
                try:
                    user_obj = User.objects.get(email__iexact=username_or_email)
                    resolved_username = getattr(user_obj, User.USERNAME_FIELD)
                except User.DoesNotExist:
                    # Dejar que falle normalmente
                    pass

            self.user_cache = authenticate(self.request, username=resolved_username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, SetPasswordForm,
                                       UserChangeForm, UserCreationForm)

from users.models import UserModel


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'id': "username", 'name': "username", 'placeholder': "Username or Email",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control", 'id': "password", 'name': "password", 'placeholder': "Password",
    }))

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = UserModel
        fields = ('username', 'password', 'captcha')


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': "form-control", 'id': "E-mail", 'name': "email", 'placeholder': "Email",
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'id': "username", 'name': "username", 'placeholder': "Username",
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'id': "first_name", 'name': "first_name", 'placeholder': "First name",
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'id': "last_name", 'name': "last_name", 'placeholder': "Last name",
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control", 'id': "password", 'name': "password", 'placeholder': "Password",
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control", 'id': "password", 'name': "re-password", 'placeholder': "Re-enter Password",
    }))

    class Meta:
        model = UserModel
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')


class ProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'id': "username", 'name': "username", 'placeholder': "Username", 'readonly': True,
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'id': "first_name", 'name': "first_name", 'placeholder': "First name",
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'id': "last_name", 'name': "last_name", 'placeholder': "Last name",
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': "form-control", 'id': "E-mail", 'name': "email", 'placeholder': "Email", 'readonly': True,
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input',
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'id': "phone_number", 'name': "phone_number", 'placeholder': "Phone number",
    }))

    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email', 'image', 'phone_number')


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control", 'placeholder': "Old password",
    }))

    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control", 'placeholder': "New password",
    }))

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control", 'placeholder': "Reply new password",
    }))

    class Meta:
        model = get_user_model()
        fields = ('old_password', 'new_password1', 'new_password2')


class NewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control", 'placeholder': "New password",
    }))

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control", 'placeholder': "Reply new password",
    }))

    class Meta:
        model = get_user_model()
        fields = ('new_password1', 'new_password2')


class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': "form-control", 'id': "E-mail", 'name': "email", 'placeholder': "Email",
    }))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = get_user_model()
        fields = ('email', 'captcha')

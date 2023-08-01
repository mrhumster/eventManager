import re

from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError

from accounts.models import Settings


def not_exists_username_validator(username):
    if User.objects.filter(username__iexact=username).exists():
        raise ValidationError('Имя пользователя занято')


def exists_username_validator(username):
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        raise ValidationError('Пользователь не зарегистрирован')


def correct_username_validator(username):
    """Проверка на запрещенные символы"""
    if not re.search(r'^\w+$', username):
        raise ValidationError('Имя пользователя должно состоять из латинских букв, цифр и символа подчёркивания')


def new_email_validator(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError('Пользователь с таким адресом электронной почты уже существует')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=254, widget=forms.PasswordInput, required=True, label='Текущий пароль')
    password = forms.CharField(max_length=254, widget=forms.PasswordInput, required=True, label='Пароль')
    password2 = forms.CharField(max_length=254, widget=forms.PasswordInput, required=True, label='Подтверждение пароля')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        old_password = cleaned_data.get('old_password')

        user = self.request.user

        if not user.check_password(old_password):
            self.add_error('old_password', "Не верный пароль")

        if password and password2:
            # Only do something if both fields are valid so far.
            if password != password2:
                self.add_error('password2', 'Введенные пароли не совпадают')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label='Имя пользователя')
    password = forms.CharField(max_length=254, label='Пароль', widget=forms.PasswordInput)


class SigninForm(forms.Form):
    username = forms.CharField(max_length=30,
                               required=True,
                               label='Имя пользователя',
                               validators=[not_exists_username_validator, correct_username_validator])
    password = forms.CharField(max_length=254, widget=forms.PasswordInput, required=True, label='Пароль')
    password2 = forms.CharField(max_length=254, widget=forms.PasswordInput, required=True, label='Подтверждение пароля')
    email = forms.EmailField(max_length=254, widget=forms.EmailInput, required=True, label='Адрес электронной почты',
                             validators=[validators.EmailValidator, new_email_validator])
    first_name = forms.CharField(max_length=128, label='Имя')
    last_name = forms.CharField(max_length=128, label='Фамилия')

    group = forms.CharField(widget=forms.RadioSelect())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2:
            # Only do something if both fields are valid so far.
            if password != password2:
                self.add_error('password2', 'Введенные пароли не совпадают')
                raise ValidationError("Введенные пароли не совпадают")


class UpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, widget=forms.EmailInput, required=True,
                             validators=[validators.EmailValidator])
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['closing_notice', 'comment_notice']


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, label='Имя пользователя',
                               validators=[exists_username_validator, correct_username_validator])

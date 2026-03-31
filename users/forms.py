# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from .models import User, Visitor


class SignUpForm(forms.ModelForm):
    """Форма регистрации пользователя, соответствующая HTML шаблону"""

    # Поле для имени (Ваше имя *)
    full_name = forms.CharField(
        max_length=255,
        required=True,
        label='Ваше имя *',
        widget=forms.TextInput(attrs={
            'id': 'name',
            'placeholder': 'Введите ваше имя',
            'required': True
        })
    )

    # Поле для email (Email *)
    email = forms.EmailField(
        required=True,
        label='Email *',
        widget=forms.EmailInput(attrs={
            'id': 'email',
            'placeholder': 'example@mail.com',
            'required': True
        })
    )

    # Поле для пароля (Password)
    password1 = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'id': 'phone',  # В вашем HTML id="phone" для поля пароля
            'placeholder': 'Придумайте и введите пароль'
        })
    )

    # Поле для подтверждения пароля (добавляем, но в HTML его нет)
    '''password2 = forms.CharField(
        required=True,
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'id': 'confirm_password',
            'placeholder': 'Повторите пароль',
            'style': 'display: none;'  # Скрываем, если не нужно в HTML
        })
    )'''

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password1')

    def clean_email(self):
        """Проверка на уникальность email"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_password1(self):
        """Проверка сложности пароля"""
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов')
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError('Пароль должен содержать буквы')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Пароль должен содержать цифры')
        return password

    '''def clean(self):
        """Проверка совпадения паролей"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return cleaned_data'''

    def save(self, commit=True):
        """Сохранение пользователя"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
            # Создаем профиль посетителя
            Visitor.objects.get_or_create(user=user)

        return user
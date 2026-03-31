from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import SignUpForm


# Create your views here.
def sign_up(request):
    """Регистрация пользователя"""

    if request.method == 'POST':
        print("POST данные:", request.POST)  # Для отладки

        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.full_name}!')
            return redirect('main')
        else:
            # Выводим ошибки формы
            print("Ошибки формы:", form.errors)  # Для отладки
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = SignUpForm()

    # Передаем форму в шаблон
    return render(request, 'sign_up.html', {'form': form})


def sign_in(request):
    '''if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['pass_1'] == form.cleaned_data['pass_2']:
                form.save()
                return redirect('sign_in.html')
            else:
                error = 'Повторение пароля неверно'

        else:
            error = 'Введенные данные неверны'

    form = EmailForm()
    context = {
        'form': form
    }'''
    return render(request, 'sign_in.html')


def user_profile(request):
    '''if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['pass_1'] == form.cleaned_data['pass_2']:
                form.save()
                return redirect('sign_in.html')
            else:
                error = 'Повторение пароля неверно'

        else:
            error = 'Введенные данные неверны'

    form = EmailForm()
    context = {
        'form': form
    }'''
    return render(request, 'user_profile.html')


def user_bron(request):
    '''if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['pass_1'] == form.cleaned_data['pass_2']:
                form.save()
                return redirect('sign_in.html')
            else:
                error = 'Повторение пароля неверно'

        else:
            error = 'Введенные данные неверны'

    form = EmailForm()
    context = {
        'form': form
    }'''
    return render(request, 'user_bron.html')

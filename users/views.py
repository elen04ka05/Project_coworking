from django.shortcuts import render

# Create your views here.
def sign_up(request):
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
    return render(request, 'sign_up.html')


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
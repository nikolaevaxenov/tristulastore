from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import CreateUserForm


def registrationPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Аккаунт успешно создан!")

            redirect('loginPage')

    context = {'form': form}
    return render(request, 'account/registration.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['logged_in'] = True
            return redirect('index')
        else:
            messages.info(request, "Логин или пароль неверны!")
            return render(request, 'account/login.html')

    return render(request, 'account/login.html')


def logoutUser(request):
    logout(request)
    return redirect('loginPage')


def accountPage(request):
    if request.session.get('logged_in') in (False, None):
        return redirect('loginPage')
    return render(request, 'account/account.html')

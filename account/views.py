from django.shortcuts import render


def registration(request):
    return render(request, 'account/registration.html')


def login(request):
    return render(request, 'account/login.html')


def account(request):
    return render(request, 'account/account.html')

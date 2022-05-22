from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from store.models import Order
from store.views import getCartProductsQuantity

from .forms import CreateUserForm


def registrationPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Аккаунт успешно создан!")

            return redirect('loginPage')

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

            userDB = User.objects.filter(username=user.username).first().id
            request.session['user_id'] = userDB

            cart = Order.objects.filter(user_id=userDB, status="cart").first()
            if not cart:
                cart = Order(status="cart", user_id=userDB)
                cart.save()
            request.session['cart_id'] = cart.id

            getCartProductsQuantity(request)
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

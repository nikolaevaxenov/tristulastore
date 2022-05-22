from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from store.models import Product, Order, Order_Product
from store.views import getCartProductsQuantity

from .models import User_Details, User_Address, User_Card
from .forms import CreateUserForm, CreateUpdateUserDetails, CreateUpdateUserAddress, CreateUpdateUserCard


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


@login_required(login_url='/login/')
def createUpdateUserDetails(request):
    if request.method == 'POST':
        form = CreateUpdateUserDetails(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            middle_name = form.cleaned_data['middle_name']
            phone_number = form.cleaned_data['phone_number']

            obj, created = User_Details.objects.update_or_create(
                user_id=request.session['user_id'], defaults={'first_name': first_name, 'last_name': last_name, 'middle_name': middle_name, 'phone_number': phone_number})
            return redirect('accountPage')


@login_required(login_url='/login/')
def createUpdateUserAddress(request):
    if request.method == 'POST':
        form = CreateUpdateUserAddress(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            street = form.cleaned_data['street']
            house = form.cleaned_data['house']
            housing = form.cleaned_data['housing']
            apartment = form.cleaned_data['apartment']
            intercom_code = form.cleaned_data['intercom_code']

            obj, created = User_Address.objects.update_or_create(
                user_id=request.session['user_id'], defaults={'city': city, 'street': street, 'house': house, 'housing': housing, 'apartment': apartment, 'intercom_code': intercom_code})
            return redirect('accountPage')


@login_required(login_url='/login/')
def createUpdateUserCard(request):
    if request.method == 'POST':
        form = CreateUpdateUserCard(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            expiry_date = form.cleaned_data['expiry_date']
            cvc_code = form.cleaned_data['cvc_code']

            obj, created = User_Card.objects.update_or_create(
                user_id=request.session['user_id'], defaults={'card_number': card_number, 'expiry_date': expiry_date, 'cvc_code': cvc_code})
            return redirect('accountPage')


@login_required(login_url='/login/')
def accountPage(request):
    try:
        userDetails = User_Details.objects.get(
            user_id=request.session['user_id'])
        userDetailsForm = CreateUpdateUserDetails(
            initial={'first_name': userDetails.first_name, 'last_name': userDetails.last_name, 'middle_name': userDetails.middle_name, 'phone_number': int(userDetails.phone_number)})
    except User_Details.DoesNotExist:
        userDetails = None
        userDetailsForm = CreateUpdateUserDetails()

    try:
        userAddress = User_Address.objects.get(
            user_id=request.session['user_id'])
        userAddressForm = CreateUpdateUserAddress(
            initial={'city': userAddress.city, 'street': userAddress.street, 'house': userAddress.house, 'housing': userAddress.housing, 'apartment': userAddress.apartment, 'intercom_code': userAddress.intercom_code})
    except User_Address.DoesNotExist:
        userAddress = None
        userAddressForm = CreateUpdateUserAddress()

    try:
        userCard = User_Card.objects.get(user_id=request.session['user_id'])
        userCardForm = CreateUpdateUserCard(initial={
            'card_number': int(userCard.card_number)})
    except User_Card.DoesNotExist:
        userCard = None
        userCardForm = CreateUpdateUserCard()

    try:
        orders = Order.objects.filter(
            user_id=request.session["user_id"], status="progress").all()
        order_products = [Order_Product.objects.filter(
            order_id=order.id).all() for order in orders]
        products = [[[Product.objects.get(id=product.product_id), product.quantity, product.order_id]
                     for product in order] for order in order_products]

        totalPrices = []
        for order_product in order_products:
            sum = 0
            for product in order_product:
                sum = sum + \
                    (Product.objects.get(
                        id=product.product_id).sale_price * product.quantity)
            totalPrices.append(sum)

        products = zip(products, totalPrices)

    except User_Card.DoesNotExist:
        products = None

    return render(request, 'account/account.html', {'products': products, 'userDetails': userDetails, 'userAddress': userAddress, 'userCard': userCard, 'UserDetailsForm': userDetailsForm, 'UserAddressForm': userAddressForm, 'UserCardForm': userCardForm})

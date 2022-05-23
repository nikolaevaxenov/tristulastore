from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from store.models import Product, Order, Order_Product
from store.views import getCartProductsQuantity

from .models import User_Details, User_Address, User_Card
from .forms import CreateUserForm, CreateUpdateUserDetails, CreateUpdateUserAddress, CreateUpdateUserCard, ChangePassword


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
        userDetailsForm = CreateUpdateUserDetails(request.POST)
        if userDetailsForm.is_valid():
            first_name = userDetailsForm.cleaned_data['first_name']
            last_name = userDetailsForm.cleaned_data['last_name']
            middle_name = userDetailsForm.cleaned_data['middle_name']
            phone_number = userDetailsForm.cleaned_data['phone_number']

            obj, created = User_Details.objects.update_or_create(
                user_id=request.session['user_id'], defaults={'first_name': first_name, 'last_name': last_name, 'middle_name': middle_name, 'phone_number': phone_number})
            return redirect('accountPage')
        else:
            try:
                userDetails = User_Details.objects.get(
                    user_id=request.session['user_id'])
            except User_Details.DoesNotExist:
                userDetails = None

            try:
                userAddress = User_Address.objects.get(
                    user_id=request.session['user_id'])
                userAddressForm = CreateUpdateUserAddress(
                    initial={'city': userAddress.city, 'street': userAddress.street, 'house': userAddress.house, 'housing': userAddress.housing, 'apartment': userAddress.apartment, 'intercom_code': userAddress.intercom_code})
            except User_Address.DoesNotExist:
                userAddress = None
                userAddressForm = CreateUpdateUserAddress()

            try:
                userCard = User_Card.objects.get(
                    user_id=request.session['user_id'])
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

            return render(request, 'account/account.html', {'products': products, 'userDetails': userDetails, 'userAddress': userAddress, 'userCard': userCard, 'UserDetailsForm': userDetailsForm, 'UserAddressForm': userAddressForm, 'UserCardForm': userCardForm, 'state': 1})


@login_required(login_url='/login/')
def createUpdateUserAddress(request):
    if request.method == 'POST':
        userAddressForm = CreateUpdateUserAddress(request.POST)
        if userAddressForm.is_valid():
            city = userAddressForm.cleaned_data['city']
            street = userAddressForm.cleaned_data['street']
            house = userAddressForm.cleaned_data['house']
            housing = userAddressForm.cleaned_data['housing']
            apartment = userAddressForm.cleaned_data['apartment']
            intercom_code = userAddressForm.cleaned_data['intercom_code']

            obj, created = User_Address.objects.update_or_create(
                user_id=request.session['user_id'], defaults={'city': city, 'street': street, 'house': house, 'housing': housing, 'apartment': apartment, 'intercom_code': intercom_code})
            return redirect('accountPage')
        else:
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
            except User_Address.DoesNotExist:
                userAddress = None

            try:
                userCard = User_Card.objects.get(
                    user_id=request.session['user_id'])
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

            return render(request, 'account/account.html', {'products': products, 'userDetails': userDetails, 'userAddress': userAddress, 'userCard': userCard, 'UserDetailsForm': userDetailsForm, 'UserAddressForm': userAddressForm, 'UserCardForm': userCardForm, 'state': 2})


@login_required(login_url='/login/')
def createUpdateUserCard(request):
    if request.method == 'POST':
        userCardForm = CreateUpdateUserCard(request.POST)
        if userCardForm.is_valid():
            card_number = userCardForm.cleaned_data['card_number']
            expiry_date = userCardForm.cleaned_data['expiry_date']
            cvc_code = userCardForm.cleaned_data['cvc_code']

            obj, created = User_Card.objects.update_or_create(
                user_id=request.session['user_id'], defaults={'card_number': card_number, 'expiry_date': expiry_date, 'cvc_code': cvc_code})
            return redirect('accountPage')
        else:
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
                userCard = User_Card.objects.get(
                    user_id=request.session['user_id'])
            except User_Card.DoesNotExist:
                userCard = None

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

            return render(request, 'account/account.html', {'products': products, 'userDetails': userDetails, 'userAddress': userAddress, 'userCard': userCard, 'UserDetailsForm': userDetailsForm, 'UserAddressForm': userAddressForm, 'UserCardForm': userCardForm, 'state': 3})


@login_required(login_url='/login/')
def accountPage(request):
    state = 0

    if request.method == 'POST':
        changePasswordForm = ChangePassword(request.POST)
        if changePasswordForm.is_valid():
            oldPassword = changePasswordForm.cleaned_data['oldPassword']
            newPassword = changePasswordForm.cleaned_data['newPassword']
            confPassword = changePasswordForm.cleaned_data['confPassword']

            user = authenticate(username=request.user, password=oldPassword)

            if user is not None:
                user.set_password(confPassword)
                user.save()

            return redirect('accountPage')
        else:
            state = 4
    else:
        changePasswordForm = ChangePassword()

    user_id = request.session.get('user_id')
    try:
        userDetails = User_Details.objects.get(
            user_id=user_id)
        userDetailsForm = CreateUpdateUserDetails(
            initial={'first_name': userDetails.first_name, 'last_name': userDetails.last_name, 'middle_name': userDetails.middle_name, 'phone_number': int(userDetails.phone_number)})
    except User_Details.DoesNotExist:
        userDetails = None
        userDetailsForm = CreateUpdateUserDetails()

    try:
        userAddress = User_Address.objects.get(
            user_id=user_id)
        userAddressForm = CreateUpdateUserAddress(
            initial={'city': userAddress.city, 'street': userAddress.street, 'house': userAddress.house, 'housing': userAddress.housing, 'apartment': userAddress.apartment, 'intercom_code': userAddress.intercom_code})
    except User_Address.DoesNotExist:
        userAddress = None
        userAddressForm = CreateUpdateUserAddress()

    try:
        userCard = User_Card.objects.get(user_id=user_id)
        userCardForm = CreateUpdateUserCard(initial={
            'card_number': int(userCard.card_number)})
    except User_Card.DoesNotExist:
        userCard = None
        userCardForm = CreateUpdateUserCard()

    try:
        orders = Order.objects.filter(
            user_id=user_id, status="progress").all()
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

    return render(request, 'account/account.html', {'products': products, 'userDetails': userDetails, 'userAddress': userAddress, 'userCard': userCard, 'UserDetailsForm': userDetailsForm, 'UserAddressForm': userAddressForm, 'UserCardForm': userCardForm, 'ChangePasswordForm': changePasswordForm, 'state': state})

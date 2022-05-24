from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from account.models import User_Details, User_Address, User_Card

from .models import Product, Order, Order_Product, Feedback, Event
from .forms import CreateUpdateUserDetails, FeedbackForm

import json


def getCartProductsQuantity(request):
    if 'logged_in' in request.session:
        order_products = Order_Product.objects.filter(
            order_id=request.session['cart_id']).all()
        sum = 0
        for order_product in order_products:
            sum = sum + order_product.quantity
        request.session['cart_quantity'] = sum

        return sum


def getCartProductsTotalPrice(request):
    if request.session['logged_in']:
        order_products = Order_Product.objects.filter(
            order_id=request.session['cart_id']).all()
        sum = 0
        for order_product in order_products:
            sum = sum + \
                (Product.objects.get(
                    id=order_product.product_id).sale_price * order_product.quantity)

    return sum


def index(request):
    types = {"Стул": "chair",
             "Шкаф": "closet",
             "Стол": "table",
             "Тумба": "pedestal"}

    products = [[i[0], i[1], i[2], i[3][13:], types[i[4]], i[5]] for i in Product.objects.exclude(
        sale_price=None).values_list('name', 'description', 'sale_price', 'photo', 'product_type', 'id')[:5]]

    return render(request, 'store/index.html', {'products': products})


@login_required(login_url='/login/')
def cartDetails(request):
    if request.method == 'POST':
        form = CreateUpdateUserDetails(request.POST)
        print(form)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            middle_name = form.cleaned_data['middle_name']
            phone_number = form.cleaned_data['phone_number']

            city = form.cleaned_data['city']
            street = form.cleaned_data['street']
            house = form.cleaned_data['house']
            housing = form.cleaned_data['housing']
            apartment = form.cleaned_data['apartment']
            intercom_code = form.cleaned_data['intercom_code']

            card_number = form.cleaned_data['card_number']
            expiry_date = form.cleaned_data['expiry_date']
            cvc_code = form.cleaned_data['cvc_code']

            obj, created = User_Details.objects.update_or_create(
                user_id=request.session['user_id'], defaults={'first_name': first_name, 'last_name': last_name, 'middle_name': middle_name, 'phone_number': phone_number})
            obj, created = User_Address.objects.update_or_create(
                user_id=request.session['user_id'], defaults={'city': city, 'street': street, 'house': house, 'housing': housing, 'apartment': apartment, 'intercom_code': intercom_code})
            obj, created = User_Card.objects.update_or_create(
                user_id=request.session['user_id'], defaults={'card_number': card_number, 'expiry_date': expiry_date, 'cvc_code': cvc_code})

            cart = Order.objects.get(id=request.session['cart_id'])
            cart.status = "progress"
            cart.save()

            cart = Order(status="cart", user_id=request.session['user_id'])
            cart.save()
            request.session['cart_id'] = cart.id
            getCartProductsQuantity(request)

            return render(request, 'store/cart.html', {'success': True})
        else:
            try:
                userDetails = User_Details.objects.get(
                    user_id=request.session['user_id'])
            except User_Details.DoesNotExist:
                userDetails = None

            try:
                userAddress = User_Address.objects.get(
                    user_id=request.session['user_id'])
            except User_Address.DoesNotExist:
                userAddress = None

            try:
                userCard = User_Card.objects.get(
                    user_id=request.session['user_id'])
            except User_Card.DoesNotExist:
                userCard = None

            order_products = Order_Product.objects.filter(
                order_id=request.session['cart_id']).all()
            products = [[Product.objects.get(id=product.product_id), Product.objects.get(id=product.product_id).photo.name[13:], product.quantity, product.id]
                        for product in order_products]

            return render(request, 'store/cart.html', {'products': products, 'userDetails': userDetails, 'userAddress': userAddress, 'userCard': userCard, 'form': form})


@login_required(login_url='/login/')
def cart(request):
    if request.method == "POST":
        body = json.loads(request.body)
        if body['action'] != "update":
            product = Order_Product.objects.get(id=body['id'])
        if body['action'] == "plus":
            product.quantity = product.quantity + 1
            product.save()
        elif body['action'] == "minus":
            product.quantity = product.quantity - 1
            product.save()
        elif body['action'] == "delete":
            product.delete()

        return JsonResponse({'action': body['action'], 'totalPrice': getCartProductsTotalPrice(request), 'totalQuantity': getCartProductsQuantity(request)})

    else:
        initial_values = {}

        try:
            userDetails = User_Details.objects.get(
                user_id=request.session['user_id'])
            initial_values = initial_values | {'first_name': userDetails.first_name, 'last_name': userDetails.last_name,
                                               'middle_name': userDetails.middle_name, 'phone_number': int(userDetails.phone_number)}
        except User_Details.DoesNotExist:
            userDetails = None

        try:
            userAddress = User_Address.objects.get(
                user_id=request.session['user_id'])
            initial_values = initial_values | {'city': userAddress.city, 'street': userAddress.street, 'house': userAddress.house,
                                               'housing': userAddress.housing, 'apartment': userAddress.apartment, 'intercom_code': userAddress.intercom_code}
        except User_Address.DoesNotExist:
            userAddress = None

        try:
            userCard = User_Card.objects.get(
                user_id=request.session['user_id'])
            initial_values = initial_values | {
                'card_number': int(userCard.card_number)}
        except User_Card.DoesNotExist:
            userCard = None

        userDetailsForm = CreateUpdateUserDetails(initial=initial_values)

        order_products = Order_Product.objects.filter(
            order_id=request.session['cart_id']).all()
        products = [[Product.objects.get(id=product.product_id), Product.objects.get(id=product.product_id).photo.name[13:], product.quantity, product.id]
                    for product in order_products]

        return render(request, 'store/cart.html', {'products': products, 'userDetails': userDetails, 'userAddress': userAddress, 'userCard': userCard, 'form': userDetailsForm})


def catalog(request, product_type="empty", id=-1):
    if request.method == 'POST':
        product_id = request.POST.get('addToCartBtn')
        order_product = Order_Product.objects.filter(
            order_id=request.session['cart_id'], product_id=product_id).first()
        if not order_product:
            order_product = Order_Product(
                quantity=0, order_id=request.session['cart_id'], product_id=product_id)
            order_product.save()
        order_product.quantity = order_product.quantity + 1
        order_product.save()

    getCartProductsQuantity(request)

    types = {"chair": "Стул",
             "closet": "Шкаф",
             "table": "Стол",
             "pedestal": "Тумба"}

    if (product_type == "empty" or product_type not in types.keys()):
        id = Product.objects.filter(product_type='Стул').first().id
        product_type = "chair"
    elif id == -1:
        id = Product.objects.filter(
            product_type=types[product_type]).first().id

    products = Product.objects.filter(product_type=types[product_type]).values_list(
        'id', 'name', 'description', 'price', 'sale_price', 'photo', 'product_type')

    main_product = products.filter(id=id)[0]

    return render(request, 'store/catalog.html', {'id': id, 'main_product': main_product, 'products': products, 'product_type': product_type})


def contacts(request):
    return render(request, 'store/contacts.html')


def feedback(request):
    if request.method == 'POST':
        feedbackForm = FeedbackForm(request.POST)
        if feedbackForm.is_valid():
            subject = feedbackForm.cleaned_data['subject']
            description = feedbackForm.cleaned_data['description']

            feedback = Feedback(subject=subject, description=description)
            feedback.save()

            return render(request, 'store/feedback.html', {'feedbackForm': feedbackForm, 'success': True})
    else:
        feedbackForm = FeedbackForm()

    return render(request, 'store/feedback.html', {'feedbackForm': feedbackForm})


def events(request):
    events = Event.objects.all()
    return render(request, 'store/events.html', {'events': events})

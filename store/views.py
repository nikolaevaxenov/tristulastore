from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from store.models import Product, Order, Order_Product
import json


def getCartProductsQuantity(request):
    if request.session['logged_in']:
        order_products = Order_Product.objects.filter(
            order_id=request.session['cart_id']).all()
        sum = 0
        for order_product in order_products:
            sum = sum + order_product.quantity
        request.session['cart_quantity'] = sum


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
    products = [[i[0], i[1], i[2], i[3][13:]] for i in Product.objects.exclude(sale_price=None).values_list(
        'name', 'description', 'sale_price', 'photo')[:5]]

    return render(request, 'store/index.html', {'products': products})


@login_required(login_url='/login/')
def cart(request):
    if request.method == "POST":
        if request.POST.get('createOrder'):
            cart = Order.objects.get(id=request.session['cart_id'])
            cart.status = "progress"
            cart.save()

            cart = Order(status="cart", user_id=request.session['user_id'])
            cart.save()
            request.session['cart_id'] = cart.id
            getCartProductsQuantity(request)

            return render(request, 'store/cart.html', {'success': True})

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

        return JsonResponse({'action': body['action'], 'totalPrice': getCartProductsTotalPrice(request)})

    else:
        order_products = Order_Product.objects.filter(
            order_id=request.session['cart_id']).all()
        products = [[Product.objects.get(id=product.product_id), Product.objects.get(id=product.product_id).photo.name[13:], product.quantity, product.id]
                    for product in order_products]

        return render(request, 'store/cart.html', {'products': products})


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

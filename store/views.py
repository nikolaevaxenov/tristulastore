from django.shortcuts import render
from store.models import Product


def index(request):
    products = [[i[0], i[1], i[2], i[3][13:]] for i in Product.objects.exclude(sale_price=None).values_list(
        'name', 'description', 'sale_price', 'photo')[:5]]

    return render(request, 'store/index.html', {'products': products})


def catalog(request, product_type="empty", id=-1):
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

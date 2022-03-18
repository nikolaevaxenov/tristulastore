from django.shortcuts import render
from store.models import Product


def index(request):
    products = [[i[0], i[1], i[2], i[3][13:]] for i in Product.objects.exclude(sale_price=None).values_list(
        'name', 'description', 'sale_price', 'photo')[:5]]

    return render(request, 'store/index.html', {'products': products})


def catalog(request):
    return render(request, 'store/index.html')

from django.shortcuts import render
from timeit import default_timer
from django.http import HttpRequest, HttpResponse


def shop_index(request: HttpRequest):
    products = [
        ('Laptop', 1999)
        ('Desktop', 2999)
        ('Smartphone', 999)

    ]
    context = {
        "time_rinning": default_timer(),
        "products": products,
    }
    return render(request, 'shopapp/shop-index.html', context=context)

from django.shortcuts import render
from timeit import default_timer
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import Group
from .models import Product

def shop_index(request: HttpRequest) -> HttpResponse:
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999)
    ]
    context = {
        "time_running": default_timer(),
        "products": products,
    }
    return render(request, 'shopapp/shop-index.html', context)

def groups_list(request: HttpRequest) -> HttpResponse:
    context = {
        "groups": Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context)

def products_list(request: HttpRequest):
    context = {
        "products": Product.objects.all(),
    }
    return render(request, 'shopapp/products-list.html', context=context)
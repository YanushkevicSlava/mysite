from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import Group

from .models import Product, Order


def shop_index(request: HttpRequest):
    return render(request, 'shopapp/shop-index.html')


def groups_list(request: HttpRequest):
    context = {
        "groups": Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context)


def products_list(request: HttpRequest):
    context = {
        "products": Product.objects.all(),
    }
    return render(request, 'shopapp/products-list.html', context)


def orders_lisr(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all(),
    }
    return render(request, 'shopapp/orders-list.html', context)

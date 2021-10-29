from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from .models import Product, ProductCategory
import random


def get_basket(user):
    if user.is_authenticated:
        return sum(list(Basket.objects.filter(user=user).values_list('quantity',flat=True)))
    return 0


def index(request):
    context = {
        'products': Product.objects.all()[:4],
        'title': 'Главная',
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', context)


def contact(request):
    context = {
        'title': 'Контакты',
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', context)


def products(request, pk=None):
    category = ProductCategory.objects.all()
    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {
                'name': 'все',
                'pk': 0,
                'basket': get_basket(request.user)
            }
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)
        context = {
            'title': 'Продукты',
            'category': category,
            'products': products_list,
            'category_item': category_item,
            'basket': get_basket(request.user)
        }

        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = random.sample(list(Product.objects.all()), 1)[0]
    same_products = Product.objects.all()[3:5]
    context = {
        'title': 'Продукты',
        'category': category,
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/products.html', context=context)

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from basketapp.models import Basket
from .models import Product, ProductCategory
import random


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_product):
    products_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).select_related()[
                    :3]
    return products_list


def index(request):
    context = {
        'products': Product.objects.all()[:4],
        'title': 'Главная',
    }
    return render(request, 'mainapp/index.html', context)


def contact(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'mainapp/contact.html', context)


def products(request, pk=None, page=1):
    category = ProductCategory.objects.all()
    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {
                'name': 'все',
                'pk': 0,
            }
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)
        # page = request.GET.get('p', 1)
        paginator = Paginator(products_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        context = {
            'title': 'Продукты',
            'category': category,
            'products': products_paginator,
            'category_item': category_item,
        }

        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'title': 'Продукты',
        'category': category,
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    category = ProductCategory.objects.all()
    context = {
        'product': get_object_or_404(Product, pk=pk),
        'category': category,
    }
    return render(request, 'mainapp/product.html', context)

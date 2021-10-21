from django.shortcuts import render
from .models import Product, ProductCategory


def index(request):
    context = {
        'products': Product.objects.all()[:4],
        'title': 'Главная'
    }
    return render(request, 'mainapp/index.html', context)


def contact(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'mainapp/contact.html', context)


def products(request, pk=None):
    context = {
        'title': 'Продукты',
        'category': ProductCategory.objects.all()
    }
    return render(request, 'mainapp/products.html', context=context)

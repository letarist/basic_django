from django.db import models


class ProductCategory(models.Model):
    title = models.CharField(max_length=60, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField(max_length=60, verbose_name='Название товара')
    image = models.ImageField(upload_to='products', blank=True, verbose_name='Картинка')
    short_desc = models.CharField(max_length=100, verbose_name='Краткое описание')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return f'{self.title}({self.category.title})'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

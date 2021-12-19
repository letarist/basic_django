from django.db import models

from django.conf import settings
from django.utils.functional import cached_property
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    add_datetime = models.DateTimeField(auto_now_add=True)

    # @cached_property
    # def get_items_cached(self):
    #     return self.user.basket.select_related()

    @property
    def total_quantity(self):
        items = Basket.objects.filter(user=self.user)
        return sum(list(map(lambda x: x.quantity, items)))

    @property
    def total_cost(self):
        items = Basket.objects.filter(user=self.user)
        return sum(list(map(lambda x: x.product_cost, items)))

    @property
    def product_cost(self):
        return self.quantity * self.product.price

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

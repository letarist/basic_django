from django.db import models
from django.conf import settings

from mainapp.models import Product


# class OrderQuerySet(models.QuerySet):
#
#     def delete(self, *args, **kwargs):
#         for object in self:
#             for item in object.orderitems.select_related():
#                 item.product.quantity += item.quantity
#                 item.product.save()
#             object.is_active = False
#             object.save()
#         super().delete(*args,**kwargs)


class Order(models.Model):

    # objects = OrderQuerySet.as_manager()

    STATUS_FORMING = 'FM'
    STATUS_SEND_TO_PROCEED = 'STP'
    STATUS_PROCEEDED = 'PR'
    STATUS_PAID = 'PD'
    STATUS_DONE = 'SD'
    STATUS_CANCELED = 'SC'

    STATUSES = (
        (STATUS_FORMING, 'Формируется'),
        (STATUS_SEND_TO_PROCEED, 'На обработке'),
        (STATUS_PROCEEDED, 'Обработан'),
        (STATUS_PAID, 'Оплачен'),
        (STATUS_DONE, 'Совершен'),
        (STATUS_CANCELED, 'Отменен'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    status = models.CharField(choices=STATUSES, max_length=3, default=STATUS_FORMING, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.product_cost, items)))

    # def delete(self, *args, **kwargs):
    #     for item in self.orderitems.all():
    #         item.product.quantity += item.quantity
    #         item.product.save()
    #     self.is_active = False
    #     self.save()




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')

    @property
    def product_cost(self):
        return self.quantity * self.product.price

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)

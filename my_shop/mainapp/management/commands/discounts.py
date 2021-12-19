from datetime import timedelta

from django.db.models import Q, F, When, Case, IntegerField, DecimalField
from django.core.management.base import BaseCommand

from orderapp.models import OrderItem


class Command(BaseCommand):

    def handle(self, *args, **options):
        ACTION_1_DISCOUNT = 0.3
        ACTION_2_DISCOUNT = 0.15
        ACTION_3_DISCOUNT = 0.05
        ACTION_1_DELTA = timedelta(hours=12)
        ACTION_2_DELTA = timedelta(days=1)

        action_1 = 1
        action_2 = 2
        action_3 = 3

        action_1_condition = Q(order__updated_at__lte=F('order__created_at') + ACTION_1_DELTA)
        action_2_condition = Q(
            Q(order__updated_at__gt=F('order__created_at') + ACTION_1_DELTA) &
            Q(order__updated_at__lte=F('order__created_at') + ACTION_2_DELTA))
        action_3_condition = Q(order__updated_at__gt=F('order__created_at') + ACTION_2_DELTA)

        action_1_order = When(action_1_condition, then=action_1)
        action_2_order = When(action_2_condition, then=action_2)
        action_3_order = When(action_3_condition, then=action_3)

        action_1_price = When(action_1_condition, then=F('product__price') * F('quantity') * ACTION_1_DISCOUNT)
        action_2_price = When(action_2_condition, then=F('product__price') * F('quantity') * ACTION_2_DISCOUNT)
        action_3_price = When(action_3_condition, then=F('product__price') * F('quantity') * ACTION_3_DISCOUNT)

        orders_items_list = OrderItem.objects.all().annotate(
            action_order=Case(
                action_1_order,
                action_2_order,
                action_3_order,
                output_field=IntegerField(),
            )
        ).annotate(
            discount_price=Case(
                action_1_price,
                action_2_price,
                action_3_price,
                output_field=DecimalField(),
            )
        )
        for item in orders_items_list:
            print(
                f'{item.action_order:3}: заказ № {item.pk:3}: {item.product.title:15}: {item.discount_price:6.2f}: '
                f'{item.order.updated_at - item.order.created_at}')

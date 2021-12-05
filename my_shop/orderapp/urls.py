from django.urls import path
from orderapp import views as orderapp

app_name = 'orderapp'
urlpatterns = [
    path('', orderapp.OrderListView.as_view(), name='order_list'),
    path('create/', orderapp.OrderCreateView.as_view(), name='order_create'),
    path('read/<int:pk>/', orderapp.OrderDetailView.as_view(), name='order_read'),
    path('update/<int:pk>/', orderapp.OrderEditView.as_view(), name='order_update'),
    path('delete/<int:pk>/', orderapp.OrderDeleteView.as_view(), name='delete'),
    path('cancel/forming/<int:pk>/', orderapp.order_forming_complete, name='forming_cancel'),
    path('product/price/<int:pk>/', orderapp.product_price, name='product_price'),
]

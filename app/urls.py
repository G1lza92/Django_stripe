from django.urls import path

from .views import (CancelView, SuccessView, add_to_order, buy_item,
                    delete_from_order, item_detail, item_list, order_detail,
                    orders_list, pay_for_order)

app_name = 'app'

urlpatterns = [
    path('', item_list, name='item_list'),
    path('item/<int:pk>/', item_detail, name='item_detail'),
    path('add-to-order/<int:pk>/', add_to_order, name='add_to_order'),
    path('delete-from-order/<int:pk>/', delete_from_order, name='delete_from_order'),
    path('orders-list/', orders_list, name='orders_list'),
    path('order-detail/<int:pk>/', order_detail, name='order_detail'),
    path('buy-order/<int:pk>/', pay_for_order, name='buy_order'),
    path('success/<int:pk>/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('buy_item/<int:pk>/', buy_item, name='buy_item'),
]

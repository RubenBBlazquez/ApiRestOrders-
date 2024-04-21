from django.urls import path

from orders.infrastructure.endpoints.apis.order import OrdersAPI
from orders.infrastructure.endpoints.apis.product import ProductAPI
from orders.infrastructure.repositories.order_product_repository import OrderProductRepository
from orders.infrastructure.repositories.order_repository import OrderRepository
from orders.infrastructure.repositories.product_repository import ProductRepository
from orders.infrastructure.serializers.order_serializer import OrderSerializer
from orders.infrastructure.serializers.product_serializer import ProductSerializer

products_api = ProductAPI(ProductRepository(), ProductSerializer)
orders_api = OrdersAPI(OrderRepository(), ProductRepository(), OrderProductRepository(), OrderSerializer)

django_urls = [
    path('get_product_by_id/', products_api.get, name='get_product_by_id'),
    path('get_all_products/', products_api.get, name='get_all_products'),
    path('create_product/', products_api.post, name='create_product'),
    path('edit_product/', products_api.put, name='edit_product'),

    path('get_order_by_id/', orders_api.get, name='get_order_by_id'),
    path('get_all_orders/', orders_api.get, name='get_all_orders'),
    path('create_order/', orders_api.post, name='create_order'),
    path('edit_order/', orders_api.put, name='edit_order'),
]
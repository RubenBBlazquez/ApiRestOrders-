from django.urls import path

from orders.infrastructure.endpoints.apis.base import BaseAPI
from orders.infrastructure.repositories.product_repository import ProductRepository
from orders.infrastructure.serializers.product_serializer import ProductSerializer

products_api = BaseAPI(ProductRepository(), ProductSerializer)

django_urls = [
    path('get_product_by_id/', products_api.get, name='get_product_by_id'),
    path('get_all_products/', products_api.get, name='get_all_products'),
    path('create_product/', products_api.post, name='create_product'),
]
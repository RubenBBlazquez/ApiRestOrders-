from django.urls import path

from orders.infrastructure.endpoints.apis.base import BaseAPI
from orders.infrastructure.repositories.product_repository import ProductRepository
from orders.infrastructure.serializers.product_serializer import ProductSerializer

api = BaseAPI(ProductRepository(), ProductSerializer)

django_urls = [
    path('test/', api.get)
]
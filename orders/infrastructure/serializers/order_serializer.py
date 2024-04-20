from __future__ import annotations
from django.db import models
from rest_framework import serializers

from orders.infrastructure.models.order import OrderProduct, Order
from orders.infrastructure.serializers.base import CustomSerializer


class OrderProductSerializer(CustomSerializer, serializers.ModelSerializer):
    reference = serializers.CharField(source='product.reference', read_only=True)

    class Meta:
        model = OrderProduct
        fields = ['quantity', 'reference']

    @classmethod
    def from_model(cls, model_object: models.Model, many = False) -> OrderProductSerializer:
        return cls(model_object, many=many)


class OrderSerializer(CustomSerializer, serializers.Serializer):
    id = serializers.IntegerField()
    products = OrderProductSerializer(many=True, source='order_products')
    total_price_without_taxes = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price_with_taxes = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField()

    class Meta:
        model = Order
        fields = ['id', 'articles', 'total_price_without_taxes', 'total_price_with_taxes', 'created_at']

    @classmethod
    def from_model(cls, model_object: models.Model, many = False) -> OrderSerializer:
        return cls(model_object, many=many)

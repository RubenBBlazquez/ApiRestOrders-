from __future__ import annotations
from django.db import models
from rest_framework import serializers
from orders.infrastructure.serializers.base import CustomSerializer


class ProductSerializer(CustomSerializer, serializers.Serializer):
    id = serializers.IntegerField()
    reference = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    price_without_taxes = serializers.DecimalField(max_digits=10, decimal_places=2)
    taxes = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField()

    @classmethod
    def from_model(cls, model_object: models.Model, many=False) -> ProductSerializer:
        return cls(model_object, many=many)


from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    reference = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    price_without_taxes = serializers.DecimalField(max_digits=10, decimal_places=2)
    price_with_taxes = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField()

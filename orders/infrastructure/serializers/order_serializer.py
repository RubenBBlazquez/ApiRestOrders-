from rest_framework import serializers

from orders.infrastructure.models.order import OrderProduct, Order


class OrderProductSerializer(serializers.ModelSerializer):
    reference = serializers.CharField(source='product.reference', read_only=True)

    class Meta:
        model = OrderProduct
        fields = ['quantity', 'reference']


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    articles = OrderProductSerializer(many=True, source='order_products')
    total_price_without_taxes = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price_with_taxes = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField()

    class Meta:
        model = Order
        fields = ['id', 'articles', 'total_price_without_taxes', 'total_price_with_taxes', 'created_at']
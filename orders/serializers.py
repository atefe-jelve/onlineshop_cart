from rest_framework import serializers

class AddProductSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)


class CartSerializer(serializers.Serializer):
    product = serializers.CharField()
    quantity = serializers.IntegerField()
    total_price = serializers.IntegerField()

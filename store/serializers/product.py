from rest_framework import serializers
from store.models import Product
from decimal import Decimal

from store.serializers.productImage import ProductImageSerializer


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many = True, read_only = True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory',
                  'unit_price', 'price_with_tax', 'collection', 'images']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    @staticmethod
    def calculate_tax(product: Product):
        return product.unit_price * Decimal(1.1)
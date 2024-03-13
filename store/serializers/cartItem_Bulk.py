from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from store.models import CartItem , Product

class BaseCartItemSerializer(serializers.ModelSerializer):
    product_ids = serializers.ListField(child = serializers.IntegerField())
    quantities = serializers.ListField(child = serializers.IntegerField())

    def validate(self, data):
        product_ids = data.get('product_ids', [])
        quantities = data.get('quantities', [])

        if len(product_ids) != len(quantities):
            raise ValidationError("Number of product IDs must match number of quantities")

        invalid_ids = []
        for product_id in product_ids:
            if not Product.objects.filter(pk=product_id).exists():
                invalid_ids.append(product_id)

        if invalid_ids:
            error_message = "Invalid Product ID"
            if len(invalid_ids) > 1:
                error_message += "s"
            error_message += ": " + ", ".join(str(id) for id in invalid_ids)
            raise ValidationError(error_message)

        return data

    def get_cart_item(self, cart_id, product_id):
        try:
            return CartItem.objects.get(cart_id=cart_id, product_id=product_id)
        except CartItem.DoesNotExist:
            return None

    def create_cart_item(self, cart_id, validated_data):
        return CartItem.objects.create(cart_id=cart_id, **validated_data)

    def update_cart_item(self, cart_item, validated_data):
        for attr, value in validated_data.items():
            setattr(cart_item, attr, value)
        cart_item.save()
        return cart_item

    class Meta:
        model = CartItem
        fields = ['id' , 'product_ids' , 'quantities']


class AddCartItemBulkSerializer(BaseCartItemSerializer):
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_item = self.get_cart_item(cart_id, product_id)
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
            return cart_item
        else:
            return self.create_cart_item(cart_id, self.validated_data)

class UpdateCartItemBulkSerializer(BaseCartItemSerializer):
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        cart_item = self.get_cart_item(cart_id, product_id)
        if cart_item:
            return self.update_cart_item(cart_item, self.validated_data)
        else:
            raise serializers.ValidationError(
                'No cart item with the given product ID exists in the cart.'
            )
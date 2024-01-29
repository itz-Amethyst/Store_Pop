from rest_framework.viewsets import ModelViewSet

from store.models import CartItem
from store.serializers.cartItem import CartItemSerializer , AddCartItemSerializer , UpdateCartItemSerializer


class CartItemViewSet(ModelViewSet):
    # To remove Put method
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id = self.kwargs['cart_pk']).select_related('product')
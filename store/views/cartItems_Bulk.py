from rest_framework.viewsets import ModelViewSet

from store.models import CartItem
from store.serializers.cartItem_Bulk import UpdateCartItemBulkSerializer, AddCartItemBulkSerializer


class CartItemBulkViewSet(ModelViewSet):
    http_method_names = ['post',]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemBulkSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemBulkSerializer

    def get_serializer_context( self ):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset( self ):
        return CartItem.objects \
            .filter(cart_id = self.kwargs['cart_pk']) \
            .select_related('product')
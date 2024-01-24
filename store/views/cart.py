from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin , DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from store.models import Cart
from store.serializers.cart import CartSerializer


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer




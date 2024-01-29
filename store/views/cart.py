from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin , DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from store.models import Cart
from store.serializers.cart import CartSerializer

# GenericViewSet only get you access to get_queryset , get_object methods
class CartViewSet(GenericViewSet, CreateModelMixin ,RetrieveModelMixin ,DestroyModelMixin):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer




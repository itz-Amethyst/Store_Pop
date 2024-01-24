from rest_framework.viewsets import ModelViewSet
from store.models import ProductImage
from store.serializers.productImage import ProductImageSerializer

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    def get_queryset(self):
        return ProductImage.objects.filter(product_id = self.kwargs['product_pk'])
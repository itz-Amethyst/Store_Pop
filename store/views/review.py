from rest_framework.viewsets import ModelViewSet
from store.models import Review
from store.serializers.review import ReviewSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    # Reads the id of product from url and send it to serializer for avoiding to fill the product id by manual in request
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}



from rest_framework.permissions import IsAdminUser , IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from store.models import Customer , Order
from store.serializers.order import UpdateOrderSerializer , OrderSerializer , CreateOrderSerializer


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data = request.data, context = {'user_id': self.request.user.id})
        serializer.is_valid(raise_exception = True)
        order = serializer.save()

        # To fill the datas in return by passing the returned data in save serializer to basic to fill the entries
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    # def get_serializer_context(self):
    #     return {'user_id': self.request.user.id}

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        customer_id = Customer.objects.only('id').get(user_id = user.id)
        return Order.objects.filter(customer_id = customer_id)
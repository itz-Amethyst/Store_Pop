from requests import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser , IsAuthenticated , AllowAny
from rest_framework.viewsets import ModelViewSet

from store.models import Customer
from store.permissions import ViewCustomerHistoryPermission
from store.serializers.customer import CustomerSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated]

    # If detail is set to false it will only available in list getaway not f.e.g get_product_by_id route
    @action(detail = False, methods = ['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        # To unpack tuple
        customer = Customer.objects.get(user_id = request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


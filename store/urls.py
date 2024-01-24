from rest_framework_nested import routers
from store.views.product import ProductViewSet
from store.views.collection import CollectionViewSet
from store.views.cart import CartViewSet
from store.views.customer import CustomerViewSet
from store.views.order import OrderViewSet
from store.views.review import ReviewViewSet
from store.views.cartItem import CartItemViewSet
from store.views.productImage import ProductImageViewSet

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('collections', CollectionViewSet)
router.register('carts', CartViewSet)
router.register('customers', CustomerViewSet)
router.register('orders', OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', ReviewViewSet,
                         basename='product-reviews')
products_router.register('images', ProductImageViewSet, basename = 'product-images')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', CartItemViewSet, basename='cart-items')

# URLConf
urlpatterns = router.urls + products_router.urls + carts_router.urls

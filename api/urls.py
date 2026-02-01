from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from product.views import product_view, category_view
from order.views import cart_view, cart_item_view
from rest_framework_nested import routers

router = DefaultRouter()
router.register('product', product_view)
router.register('category', category_view)
router.register('cartview', cart_view)
router.register('cartitemview', cart_item_view,basename='cartitem')

product_router = routers.NestedDefaultRouter(router, 'product', lookup = 'products')
product_router.register('reviews',product_view, basename='pro_view')

cart_router = routers.NestedDefaultRouter(router, 'cartitemview', lookup = 'cart')
cart_router.register('items', cart_item_view, basename='cartitem')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(cart_router.urls)),
    path('', include(product_router.urls))
]

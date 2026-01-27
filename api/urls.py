from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from product.views import product_view, category_view
from order.views import cart_view

router = DefaultRouter()
router.register('product', product_view)
router.register('category', category_view)
router.register('cartview', cart_view)
urlpatterns = router.urls
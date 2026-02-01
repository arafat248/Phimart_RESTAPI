from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from .serializer import cart_serial, cartitem_serial, addcartitem_serial, up_da_serial
from .models import Cart, CartItem
from rest_framework.permissions import DjangoModelPermissions

# Create your views here.
class cart_view(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = cart_serial
    permission_classes = [DjangoModelPermissions]

class cart_item_view(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return addcartitem_serial
        elif self.request.method == 'PATCH':
            return up_da_serial
        return cartitem_serial
    
    def get_serializer_context(self):
        return{'cart_id' : self.kwargs['cart_pk']}
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])

from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from .serializer import cart_serial, cartitem_serial, addcartitem_serial, up_da_serial, OrderSerial, CreateOrderSerial, UpdateOrderSerial, EmptySerial
from .models import Cart, CartItem, OrderItem, Order
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from order.services import OrderService
from rest_framework.response import Response

class cart_view(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    #queryset = Cart.objects.all()
    serializer_class = cart_serial
    #permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(users=self.request.user)
    
    def get_queryset(self):
        return Cart.objects.filter(users = self.request.user)

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

class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch', 'option', 'head']

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order, user=request.user)
        return Response({'status': 'Order_canceled'})
    
    @action(detail=True, methods= ['PATCh'])
    def Update_Cancel(self, request, pk=None):
        order=self.get_object()
        serializer = UpdateOrderSerial(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status':'order canceled'})

    def get_permissions(self):
        if self.request.method =='DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'cancel':
            return EmptySerial
        if self.request.method=='POST':
            return CreateOrderSerial
        elif self.request.method == 'PATCH':
            return UpdateOrderSerial
        return OrderSerial
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'user': self.request.user}
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)


from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from .models import Product, Category, ProductImage
from product.serializer import product_serial, category_serial, image_serial
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.permissions import DjangoModelPermissions

###### viewset #####
class product_view(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = product_serial
    permission_classes = [DjangoModelPermissions]
    
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock > 10:
            return Response({'message': "stock more then 10 could not be deleted"})
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)

class category_view(ModelViewSet):
    queryset = Category.objects.annotate(product_count = Count('products')).all()
    serializer_class = category_serial
    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        if category.product_count >= 1:
            return Response({'message':"have more product"})
        self.perform_destroy(category)
        return Response(status=status.HTTP_204_NO_CONTENT)


class image_view(ModelViewSet):
    serializer_class = image_serial
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['products_pk'])

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs['products_pk'])
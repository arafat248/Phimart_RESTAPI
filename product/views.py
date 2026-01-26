from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from rest_framework.views import APIView
from .models import Product, Category
from product.serializer import product_serial, category_serial
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

# Create your views here
# class view_specific_product(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)  # fetch once
#         serializer = product_serial(product)
#         return Response(serializer.data)
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)  # fetch once
#         serializer = product_serial(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)  # fetch once
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class view_category(APIView):
#     def get(self, request, id):
#             category = get_object_or_404(Category, pk=id)
#             serializer = category_serial(category)
#             return Response(serializer.data)
#     def put(self, request, id):
#             category = get_object_or_404(Category, pk=id)
#             serializer = category_serial(category, data = request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)
#     def delete(self, request, id):
#             category = get_object_or_404(Category, pk=id)
#             category.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)

# class all_category(APIView):
#     def get(self, request):
#         category = Category.objects.annotate(product_count=Count('products'))
#         serializer = category_serial(category, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = category_serial(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    #######mixing and generic ######
# class get_post_product(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = product_serial

# class get_put_delete_product(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = product_serial
#     lookup_field = 'id'


# class get_put_delete_category(RetrieveUpdateDestroyAPIView):  #get, put, delete
#     queryset = Category.objects.all()
#     serializer_class = category_serial
#     lookup_field = 'id'

# class get_post_category(ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = category_serial


###### viewset #####
class product_view(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = product_serial
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
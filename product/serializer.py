from rest_framework import serializers
from .models import Product, Category

class product_serial(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class category_serial(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']
    product_count = serializers.IntegerField(read_only = True)
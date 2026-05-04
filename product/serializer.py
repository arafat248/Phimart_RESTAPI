from rest_framework import serializers
from .models import Product, Category, ProductImage

class image_serial(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ProductImage
        fields = ['id', 'image']
        #ref_name = 'imageserializer'
        
class product_serial(serializers.ModelSerializer):
    images = image_serial(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category',
                    'create_at', 'update_at', 'images']

class category_serial(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']
    product_count = serializers.IntegerField(read_only = True)

# 
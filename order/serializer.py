from rest_framework import serializers
from order.models import Cart, CartItem
from product.models import Product
from product.serializer import product_serial


class simpleProductSerial(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class addcartitem_serial(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']
    def save(self):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id = cart_id, **self.validated_data)
        return self.instance
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f'Product with id {value} does not exixtx')
        return value

class cartitem_serial(serializers.ModelSerializer):
    product = simpleProductSerial()
    total_price = serializers.SerializerMethodField(method_name = 'get_total_price')
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
    
    def get_total_price(self, cart_item : CartItem):
        return cart_item.product.price * cart_item.quantity

class cart_serial(serializers.ModelSerializer):
    items = cartitem_serial(many = True, read_only = True)
    total_price = serializers.SerializerMethodField(method_name = 'get_total_price')
    class Meta:
        model = Cart
        fields = ['id', 'users', 'items', 'total_price']

    def get_total_price(self, cart : Cart):
        return sum([item.product.price * item.quantity for item in cart.items.all()])
    
class up_da_serial(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
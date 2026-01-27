from rest_framework import serializers
from order.models import Cart


class cart_serial(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'users']
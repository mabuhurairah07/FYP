from rest_framework import serializers
from .models import Cart
from product_details.models import Product
from product_details.serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['cart_id', 'user_data', 'product', 'quantity']

class AddtoCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user_data', 'product', 'quantity']

class DSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['cart_id']
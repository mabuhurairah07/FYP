from rest_framework import serializers
from .models import *

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentDetails
        fields = "__all__"
        
class AddShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentDetails
        fields = "__all__"

class AddOrderSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class UpdateOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    payment_type = serializers.CharField()

class ViewOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_type', 'total_bill', 'bill_payed', 'discount']
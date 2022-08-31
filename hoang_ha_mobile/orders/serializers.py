from rest_framework import serializers
from orders.models import Order

class OrderChargeUpdate(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'charge_status'
        ]


class OrderStatusUpdate(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'status'
        ]
        
        
class OrderChargeId(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'charge_id'
        ]
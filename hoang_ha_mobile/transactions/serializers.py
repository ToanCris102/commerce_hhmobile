from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [ 
            'type',
            'net',
            'amount',
            'currency',
            'unit',
            'fee',
            'description',
            'payment_id',
            'order',
            'customer',
            'available_on'    
        ]

from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [ 
            'type',
            'net',
            'amount',
            'fee',
            'description',
            'payment_id',
            'order',
            'customer',
            'available_on'    
        ]

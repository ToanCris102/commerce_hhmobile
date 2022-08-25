from django.db import models
from orders.models import Order
from django.contrib.auth import get_user_model
User = get_user_model()


TYPE_CHOICES = [
    ("charge", "charge"),
    ("refund", "refund"),
]

class Transaction(models.Model):
    type = models.CharField(choices=TYPE_CHOICES, max_length=50)
    net = models.CharField(max_length=50)
    amount = models.CharField(max_length=50)
    fee = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True)
    payment_id = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)    
    customer = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    available_on = models.CharField(max_length=20)
    

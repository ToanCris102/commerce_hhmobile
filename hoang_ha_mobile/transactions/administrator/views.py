from ..models import Transaction
from .serializers import TransactionSerializer

def create_transaction(*args, **kwargs):
    TransactionSerializer(data=args)
    TransactionSerializer.is_valid(raise_exception=True)    
    TransactionSerializer.save()
    # Transaction.objects.create(TransactionSerializer.data)
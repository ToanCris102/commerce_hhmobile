from .serializers import TransactionSerializer


def create_transaction( data):
    try:
        instance = TransactionSerializer(data=data)
        instance.is_valid(raise_exception=True)    
        instance.save()
        # print(instance.data)
    except Exception as e:
        print(e)
        
    
    # Transaction.objects.create(TransactionSerializer.data)
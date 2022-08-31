from .serializers import UpdateCustomerId
from django.contrib.auth import get_user_model

User = get_user_model()


def update_customer_id(email, customer_id):    
    user = User.objects.filter(email = email)
    serializer = UpdateCustomerId(user[0], data={"customer_id": customer_id})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return serializer.data


def get_user(email):
    user = User.objects.filter(email = email)
    
    return user
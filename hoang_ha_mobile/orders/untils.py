from .serializers import OrderChargeUpdate
from .models import Order


def update_status_charge(order_id):
    order = Order.objects.get(id=order_id)    
    serializer = OrderChargeUpdate(order, data={"charge_status":True})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return serializer.data
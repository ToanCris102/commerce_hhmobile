from .serializers import OrderChargeUpdate, OrderStatusUpdate, OrderChargeId
from .models import Order


def get_order_object(order_id):
    order = Order.objects.filter(id=order_id) 
    
    return order


def update_status_charge(order_id):
    order = Order.objects.get(id=order_id)    
    serializer = OrderChargeUpdate(order, data={"charge_status":True})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return serializer.data


def update_status_order(order_id, status_name):
    order = Order.objects.get(id=order_id)    
    serializer = OrderStatusUpdate(order, data={"status":status_name})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return serializer.data


def update_charge_id(order_id, charge_id):
    order = Order.objects.get(id=order_id)    
    serializer = OrderChargeId(order, data={"charge_id": charge_id})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return serializer.data
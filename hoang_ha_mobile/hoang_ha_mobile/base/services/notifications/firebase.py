from firebase_admin import messaging
from fcm_django.models import FCMDevice



def send_message_to(device_id, device, mess_data):
    if(device is not None):
        device = device        
    else:
        device = FCMDevice.objects.filter(device_id = device_id)
        
    message = messaging.Message (
        data={
            "title" : mess_data["title"],
            "body" : mess_data["body"],            
        }
    )
    
    return device.send_message(message)
    

def list_device(user_id):
    device = FCMDevice.objects.filter(user=user_id)
    
    return device


def get_device_user(user_id):
    device = FCMDevice.objects.filter(user=user_id, active=True)
    
    return device

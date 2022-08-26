from firebase_admin import credentials, messaging
# from firebase_admin.messaging import Message

import firebase_admin

from fcm_django.models import FCMDevice


def send_message_to(device_id, mess_data):
    device = FCMDevice.objects.filter(device_id = device_id)
    print(device)
    message = messaging.Message (
        data={
            "title" : mess_data["title"],
            "body" : mess_data["body"],            
        }
    )
    return device.send_message(message)
    

def list_device():
    device = FCMDevice.objects.all()
    
    return device
from firebase_admin import credentials, messaging
from fcm_django.models import FCMDevice
from dotenv import load_dotenv
import firebase_admin
import os

# setting
load_dotenv()
cred = credentials.Certificate(os.getenv('PATH_CERTIFICATION'))
FIREBASE_APP = firebase_admin.initialize_app(cred)



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

from rest_framework_simplejwt import authentication
from rest_framework.views import APIView
from rest_framework import status, response, permissions

from hoang_ha_mobile.base.services.notifications.firebase import send_message_to, list_device

from .serializers import FCMDeviceSerializer



class SendMessageToClient(APIView):
    def post(self, *args, **kwargs):
        device_id = kwargs['device_id']
        mess_data = self.request.data['mess_data']
        send_message_to(device_id, mess_data)
        
        return response.Response(status=status.HTTP_200_OK)
    
    
class ListDeviceAPI(APIView):
    # authentication_classes = [authentication.JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
        
    def get(self, request, *args, **kwargs):
        data = list_device()
        serializer = FCMDeviceSerializer(data, many=True)

        return response.Response(data=serializer.data, status=status.HTTP_200_OK)
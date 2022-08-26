from dataclasses import field
from rest_framework import serializers
from fcm_django.models import FCMDevice

class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        # fields = [
        #     "id",
        #     "name",
        #     "user",
            
        # ]
        fields = '__all__'
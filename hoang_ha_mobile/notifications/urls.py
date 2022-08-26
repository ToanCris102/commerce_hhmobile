from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from django.urls import path
from . import views

urlpatterns = [
    path('devices/', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name="create_fcm_device"),
    path('devices/list/', views.ListDeviceAPI.as_view(), name="list_fcm_device"),
    path('devices/<int:device_id>/message/', views.SendMessageToClient.as_view(), name="send_message"),
]
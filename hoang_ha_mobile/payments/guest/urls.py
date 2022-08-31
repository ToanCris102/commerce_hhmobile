from django.urls import path, include
from . import views

urlpatterns = [
    path('webhook/', views.webhook),
    path('checkout/<int:order_id>/', views.CheckoutOrderAPIView.as_view(), name='checkout'), 
]
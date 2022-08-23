from django.urls import path, include
from . import views

urlpatterns = [
    path('webhook/', views.webhook),
    path('payment-method/', views.create_payment_method.as_view(), name='payment_method'),
    path('payment-method/<str:payment_method_id>', views.DeletePaymentMethod.as_view(), name='payment_method_detach'),
]
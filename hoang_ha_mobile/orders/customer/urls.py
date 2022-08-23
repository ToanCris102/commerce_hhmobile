from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.ListCreateOrderAPIView.as_view(), name='create_order'),  
    path('<int:order_id>/checkout/', views.CheckoutOrderAPIView.as_view(), name='checkout'),  
]
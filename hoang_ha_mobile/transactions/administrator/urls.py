from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.TransactionListAPIView.as_view(), name="transaction_list"),
]
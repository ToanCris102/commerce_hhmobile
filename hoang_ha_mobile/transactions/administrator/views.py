from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt import authentication
from ..models import Transaction
from .serializers import TransactionSerializer


class TransactionListAPIView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ['-available_on']
    filterset_fields = ['amount', 'order', 'customer']
    
    # def get_queryset(self):
    #     self.queryset = Transaction.objects.all()
    #     return super().get_queryset()




from rest_framework import generics, permissions
from rest_framework_simplejwt import authentication
from ..models import Transaction
from .serializers import TransactionSerializer


class TransactionListAPIView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    # def get_queryset(self):
    #     self.queryset = Transaction.objects.all()
    #     return super().get_queryset()




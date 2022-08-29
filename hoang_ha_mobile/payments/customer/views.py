from rest_framework import status, response, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics

from rest_framework_simplejwt import authentication

from orders.models import Order

from hoang_ha_mobile.base.services.payments.stripe.views \
import  setup_payment_intent, list_payment_method, detach_payment_method, \
webhook_stripe, checkout, refund_payment


    
class create_payment_method(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, *args, **kwargs):
        email = self.request.user.email
        # if(self.request.user.email is not None):
        if(email is not None):
            payment_intent = setup_payment_intent(email)
            data =  {
                        "client_secret": payment_intent
                    }
            
            return response.Response(data=data, status = status.HTTP_201_CREATED)
        
        return response.Response(data={"message": "Mission fail"}, status = status.HTTP_404_NOT_FOUND)
        
    def get(self, *args, **kwargs):
        email = self.request.user.email
        if(email is not None):
            list_pm = list_payment_method(email)
            data = {
                "methods": list_pm
            }
            
            return response.Response(data=data, status = status.HTTP_201_CREATED)
        
        return response.Response(data={"message": "Mission fail"}, status = status.HTTP_404_NOT_FOUND)


class DeletePaymentMethod(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, *args, **kwargs):
        payment_method_id = self.kwargs['payment_method_id']
        data = detach_payment_method(payment_method_id)
        if(data['status'] == False):
            return response.Response(data = data['data'], status = status.HTTP_400_BAD_REQUEST)
        
        return response.Response(status = status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def webhook(request):
    event = None
    payload = request.body    
    sig_header = request.headers['STRIPE_SIGNATURE']
    webhook_stripe(payload, sig_header, event)

    return response.Response(data={"success": "True"})
    
    
class CheckoutOrderAPIView(generics.CreateAPIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):        
        self.queryset = Order.objects.filter(created_by=self.request.user.id)
        
        return super().get_queryset()    
    
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        data = checkout(request.data["payment_method_id"], order_id)       
        if(data['status'] == False):            
            return response.Response(data=data['data'], status=status.HTTP_400_BAD_REQUEST)
        
        return response.Response(data=data, status=status.HTTP_201_CREATED)
        
        
class RefundOrderAPIView(generics.CreateAPIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):        
        self.queryset = Order.objects.filter(created_by=self.request.user.id, status='processing')
        
        return super().get_queryset()    
    
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        data = refund_payment(order_id)
        if(data['status'] == False):
            return response.Response(data=data['data'], status=status.HTTP_400_BAD_REQUEST)
        
        return response.Response(data=data, status=status.HTTP_201_CREATED)
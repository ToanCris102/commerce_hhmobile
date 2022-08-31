from rest_framework import status, response, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication

from hoang_ha_mobile.base.services.payments.stripe.views \
import  setup_payment_intent, list_payment_method, detach_payment_method, \
webhook_stripe, checkout, refund_payment
from hoang_ha_mobile.base.errors.bases import return_code_400

from orders.untils import update_charge_id
from orders.models import Order


    
class create_payment_method(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, *args, **kwargs):
        email = self.request.user.email
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


class CheckoutOrderAPIView(generics.CreateAPIView):    
    def post(self, request, *args, **kwargs):        
        order_id = self.kwargs['order_id']
        data = checkout(request.data["payment_method_id"], order_id)       
        if(data['status'] == False):   
            message = data['data']
            
            return return_code_400(message)
               
        print(data['data'].charges.data[0].id)
        data_return = update_charge_id(order_id, data['data'].charges.data[0].id)        
        
        return response.Response(data = data_return, status = status.HTTP_200_OK)
        
        
class RefundOrderAPIView(generics.CreateAPIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]    
    # def get_queryset(self): 
    #     self.queryset = Order.objects.filter(created_by=self.request.user.id, status='processing')      
    #     return super().get_queryset()    
    
    def post(self, request, *args, **kwargs):
        # order = Order.objects.filter(created_by=self.request.user.id, status='processing') 
        order_id = self.kwargs['order_id']
        order = Order.objects.filter(id=self.kwargs['order_id'], created_by=self.request.user.id)
        if not(order.exists()):
            message = "Order don't exist Or Other people's orders"
            
            return return_code_400(message)
        
        order = Order.objects.filter(id=self.kwargs['order_id'], status='canceled')
        if(order.exists()):
            message = "Order was refunded"
            
            return return_code_400(message)
        
        data = refund_payment(order_id)
        if(data['status'] == False):
            message = data['data']
            
            return return_code_400(message)
        
        return response.Response(status=status.HTTP_200_OK)
from rest_framework import status, response, generics
from rest_framework.decorators import api_view

from hoang_ha_mobile.base.services.payments.stripe.views import  webhook_stripe, checkout
from hoang_ha_mobile.base.errors.bases import return_code_400

from orders.untils import update_charge_id



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
    
    
@api_view(['POST'])
def webhook(request):
    event = None
    payload = request.body    
    sig_header = request.headers['STRIPE_SIGNATURE']
    webhook_stripe(payload, sig_header, event)

    return response.Response(data={"success": "True"})
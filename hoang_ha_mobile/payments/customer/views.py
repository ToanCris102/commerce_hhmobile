from rest_framework import status, response, permissions

from rest_framework.decorators import api_view
from rest_framework.views import APIView

from rest_framework_simplejwt import authentication

from hoang_ha_mobile.base.services.payments.stripe.views import setup_payment_intent, list_payment_method, detach_payment_method

import stripe

    
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
            data =  {
                        "methods": list_pm
                    }
            
            return response.Response(data=data, status = status.HTTP_201_CREATED)
        
        return response.Response(data={"message": "Mission fail"}, status = status.HTTP_404_NOT_FOUND)


class DeletePaymentMethod(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, *args, **kwargs):
        payment_method_id = self.kwargs['payment_method_id']
        print(payment_method_id)
        detach_payment_method(payment_method_id)
        
        return response.Response(status = status.HTTP_200_OK)


@api_view(['POST'])
def webhook(request):
    event = None
    payload = request.body    
    sig_header = request.headers['STRIPE_SIGNATURE']
    endpoint_secret = "whsec_8fe9a03afe2553b5c5e32a0dd8be1bfd1fd49955a0c9bc565cd194d6b1d9ccec"
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object # contains a stripe.PaymentIntent
        print('PaymentIntent was successful!')
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object # contains a stripe.PaymentMethod
        print('PaymentMethod was attached to a Customer!')
    # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event.type))
    # Handle the event
    print('Handled event type {}'.format(event['type']))

    return response.Response(data={"success": "True"})
    

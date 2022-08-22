from rest_framework.decorators import api_view
from rest_framework import status, response

import stripe


stripe.api_key = "sk_test_51LXGf3KVqGJyPIN8OybPCYaySbi95IMjawwMTafeBfinqUcgQGMkHBVCpMtx7NxMxkl83hYXB4T8jBXRV6DR6Urb00FYtmn24h"
customer = stripe.Customer.create()


# @api_view(['POST'])
def create_payment_intent(email, amount, order_id):
    # data = request.data
    # email = data['email']
    # payment_method_id = data['payment_method_id']
    customer = stripe.Customer.create(
        email = email
    )
    test_payment_intent = stripe.PaymentIntent.create(
        amount = amount, 
        currency = 'usd', 
        customer = customer['id'],
        # payment_method_type = [payment_method_id],
        setup_future_usage = 'off_session',
        automatic_payment_methods = {
            'enabled': True,
        },
        metadata = {
            'order_id': order_id,
        },
        
    )
    
    return test_payment_intent.client_secret
#     # return response.Response(status=status.HTTP_201_CREATED, data=test_payment_intent.client_secret)

def refund_payment(order_id):
    data = stripe.Charge.search(
        query = "metadata['order_id']:" + order_id
        # query = "amount=5000"
    )
    return data
    

# @api_view(['POST'])
# def save_stripe_info(request):
#     data = request.data
#     # email = data['email']
#     # payment_method_id = data['payment_method_id']
#     email = 'cris@gmail.com'
#     payment_method_id = "pm_1L2FkYJsyzcmxeMtGg6XH3z4"

#     # creating customer
#     customer = stripe.Customer.create(
#     #   email=email, payment_method=payment_method_id)
#     email=email)
#     return response.Response(status=status.HTTP_200_OK, 
#         data=   {
#             'message': 'Success', 
#             'data': {'customer_id': customer.id}
#         }   
#     )    
from rest_framework.decorators import api_view
from rest_framework import status, response
import stripe

@api_view(['POST'])
def webhook(request):
    event = None
    payload = request.body
    
    sig_header = request.headers['STRIPE_SIGNATURE']
    endpoint_secret = "whsec_8fe9a03afe2553b5c5e32a0dd8be1bfd1fd49955a0c9bc565cd194d6b1d9ccec"
                        # whsec_8fe9a03afe2553b5c5e32a0dd8be1bfd1fd49955a0c9bc565cd194d6b1d9ccec
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
    
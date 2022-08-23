import stripe

stripe.api_key = "sk_test_51LXGf3KVqGJyPIN8OybPCYaySbi95IMjawwMTafeBfinqUcgQGMkHBVCpMtx7NxMxkl83hYXB4T8jBXRV6DR6Urb00FYtmn24h"


def get_or_create_customer(email):
    customer = stripe.Customer.search(
        query ="email:'%s'" % (email)
    )     
    if(len(customer.data) < 1):
        customer = stripe.Customer.create(
            email = email
        )
        
        return customer
    
    else:
        
        return customer.data[0]


def create_payment_intent(email, amount, order_id):
    customer = get_or_create_customer(email)
    print(customer.id)
    payment_intent = stripe.PaymentIntent.create(
        amount = amount, 
        currency = 'usd', 
        customer = customer['id'],
        # payment_method_type = [payment_method_id],
        # setup_future_usage = 'off_session',
        # automatic_payment_methods = {
        #     'enabled': True,
        # },
        payment_method_types=['card'],
        metadata = {
            'order_id': order_id,
        },        
    )
    
    return payment_intent.id


def setup_payment_intent(email):
    customer = get_or_create_customer(email)
    # intent = stripe.SetupIntent.list(customer=customer.id)
    # if(len(intent) < 1):
    print(customer.id)
    intent = stripe.SetupIntent.create(
        customer = customer.id,
        payment_method_types = ["card"],
    )
            
    return intent.client_secret
    # else:
        
    #     return intent.data[0].client_secret
    
    
def list_payment_method(email):
    # customer = stripe.Customer.search(
    #     query ="email:'%s'" % (email)
    # ) 
    customer = get_or_create_customer(email)
    list = stripe.PaymentMethod.list(
        customer= customer.id,
        type="card",
    )

    return list


def detach_payment_method(payment_method_id):
    stripe.PaymentMethod.detach(
        payment_method_id,
    )    


def checkout(payment_method_id, order_id):
    payment_intent = stripe.PaymentIntent.search(
        query = "status:'requires_payment_method' AND metadata['order_id']:'%s'" % (order_id),
    )
    print(payment_intent.data[0].id)
    payment = stripe.PaymentIntent.confirm(        
        payment_intent.data[0].id,
        payment_method=payment_method_id,
    )

    return payment


def refund_payment(order_id):
    data = stripe.Charge.search(
        query = "metadata['order_id']:" + order_id
    )
    
    return data
    
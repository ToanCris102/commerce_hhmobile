from hoang_ha_mobile.base.errors.bases import exception_stripe_message

from accounts.utils import update_customer_id, get_user
from notifications.utils import push_notification_order
from transactions.utils import create_transaction
from orders.untils import update_status_charge, update_status_order, get_order_object

from dotenv import load_dotenv
import stripe, logging
import os

stripe.api_key = os.getenv('STRIPE_API_KEY')
load_dotenv()



def get_or_create_customer(email):
    user = get_user(email)
    if(user.exists() and user[0].customer_id != ''):
        return user[0].customer_id
    
    else:
        customer = stripe.Customer.create(
            email = email
        )  
        update_customer_id(email, customer['id'])
        
        return customer['id']


def create_payment_intent(email, amount, order_id, payment_method_id, account_id):
    if(account_id is not None):
        customer = get_or_create_customer(email)
        payment_intent = stripe.PaymentIntent.create(
            amount = amount*100, 
            currency = 'usd', 
            customer = customer,
            payment_method_types=['card'],        
            metadata = {
                'order_id': order_id,
                'account_id': account_id,
            },   
        )    
    else: 
        payment_intent = stripe.PaymentIntent.create(
            amount = amount*100, 
            currency = 'usd', 
            payment_method_types=['card'],        
            metadata = {
                'order_id': order_id,
            },   
        )  
          
    if (payment_method_id is not None):   
        try:
            payment = stripe.PaymentIntent.confirm(        
                payment_intent.id,
                payment_method=payment_method_id,
            ) 
            
            return {
                "data": payment,
                "status": "charge"
            }
        except stripe.error.CardError as e:
            # data = exception_stripe_message(e)            
            logging.error("A payment error occurred: {}".format(e.user_message))
            data = "A payment error occurred: {}".format(e.user_message)
        except stripe.error.InvalidRequestError as e:
            
            # logging.error("An invalid request occurred.")
            logging.error(e)
            data = "Payment medthod invalid data"
        except Exception:
            logging.error("Another problem occurred, maybe unrelated to Stripe.")
            data = "Another problem occurred, maybe unrelated to Stripe."
        else:
            logging.info("No error.")           
            
        return {
                # "data": "Payment Method invalid Data",
                "data": data,
                "status": False
            }
        
    return {
        "data": payment_intent.client_secret,
        "status": True
    }


def setup_payment_intent(email):
    customer = get_or_create_customer(email)
    # print(customer.id)
    intent = stripe.SetupIntent.create(
        customer = customer,
        payment_method_types = ["card"],
    )
         
    return intent.client_secret
    
    
def response_payment_method(list):
    data_return = []
    for item in list:
        data_return.append({
            "paymen_method_id": item.id,
            "card": {
                "brand": item.card.brand,
                "last4": item.card.last4,
                "exp_month": item.card.exp_month,
                "exp_year": item.card.exp_year,                
            }
        })
        
    return data_return
    
    
def list_payment_method(email):
    customer = get_or_create_customer(email)
    list = stripe.PaymentMethod.list(
        customer= customer,
        type="card",
    )    
    
    return response_payment_method(list.data)


def detach_payment_method(payment_method_id):
    try:
        payment_detach = stripe.PaymentMethod.detach(
            payment_method_id,
        )
        
        return {
            "data": payment_detach,
            "status": True
        }
    except Exception as e:
        return {
            "data": str(e),
            "status": False
        }


def checkout(payment_method_id, order_id):    
    payment_intent = stripe.PaymentIntent.search(
        query = "status:'requires_payment_method' AND metadata['order_id']:'%s'" % (order_id),
    )       
    if(len(payment_intent.data) < 1): 
        return {
            "data": "Don't ready for charge, Can't charge when Order was charged",
            "status": False
        }       
        
    try:
        payment = stripe.PaymentIntent.confirm(        
            payment_intent.data[0].id,
            payment_method=payment_method_id,
        )
        
        return {
            "data": payment,
            "status": True
        } 
    except Exception as e:
        
        return {
            "data": str(e),
            "status": False
        } 
            

def refund_payment(order_id):
    order = get_order_object(order_id)
    if(order.exists() and order[0].charge_id is not None):
        print(order[0].charge_id)
        charge = stripe.Charge.retrieve(order[0].charge_id)
        if(charge.refunded == True):
            return {
                "data": "Order was Refunded",
                "status": False
            } 
        else:
            data_rf = stripe.Refund.create(
                charge = charge.id,
            )
            
            return {
                "data": data_rf,
                "status": True
            }
            
    else:
        return {
            "data": "Invalid Data",
            "status": False
        } 
    
    
def retrieve_balance_transaction(bt_id):
    result = stripe.BalanceTransaction.retrieve(
        bt_id,
    )
    
    return result
    

def setup_transaction_info(charge):    
    type = charge['object']
    description = charge['id'] 
    blance_transaction_id = charge['balance_transaction']
    timetamp = charge['created']
    if(charge['refunded'] == True):
        type = 'refund'
        description = "Refund for charge: " + charge['id']
        blance_transaction_id = charge.refunds.data[0].balance_transaction
        timetamp = charge.refunds.data[0].created
        
    ba_tr = retrieve_balance_transaction(blance_transaction_id)
    try:
        data = {
            "type": type,
            "amount": charge['amount'],
            "currency": charge['currency'],
            "unit": "cent",
            "net": ba_tr['net'],
            "fee": ba_tr['fee'],
            "description": description,
            "payment_id": charge['payment_method'],
            "order": charge['metadata'].order_id,
            "customer": charge['metadata'].account_id,
            "available_on": timetamp,
        }
    except: 
        data = {
            "type": type,
            "amount": charge['amount'],
            "currency": charge['currency'],
            "unit": "cent",
            "net": ba_tr['net'],
            "fee": ba_tr['fee'],
            "description": description,
            "payment_id": charge['payment_method'],
            "order": charge['metadata'].order_id,
            "available_on": timetamp,
        }
        
    return data

    
def webhook_stripe(payload, sig_header, event):
    endpoint_secret = os.getenv('ENDPOINT_SECRET')
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

    if event.type == 'setup_intent.succeeded':
        print('PaymentIntent setup successful!')
          
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
    
    if event.type == 'charge.succeeded':
        charge = event.data.object
        update_status_charge(charge.metadata.order_id)
        data = setup_transaction_info(charge)
        create_transaction(data)
        print('Charging was successful!')
        title="Charging was secessful for order_id: " + str(charge.metadata.order_id)
        body="Amount: " + str(charge.amount / 100) + " " + charge.currency
        try:
            account_id = charge.metadata.account_id
            push_notification_order(account_id, title, body)
        except:
            pass
        
        
    if event.type == 'charge.refunded':
        charge = event.data.object
        # print(charge)
        status = "canceled"
        update_status_order(charge.metadata.order_id, status)
        data = setup_transaction_info(charge)
        create_transaction(data)
        print('Refunding was successful!')
        title="Refunding was secessful for order_id: " + str(charge.metadata.order_id)
        body="Refund Amount: " + str(charge.amount / 100) + " " + charge.currency
        try:
            account_id = charge.metadata.account_id
            push_notification_order(account_id, title, body)
        except:
            pass
        
    print('Handled event type {}'.format(event['type']))
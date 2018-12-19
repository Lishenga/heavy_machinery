from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from machinery.models import users, user_payment_status,transactions
from machinery.help import helpers
import datetime
from django.core.paginator import Paginator
import stripe
from django.conf import settings


STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY

@api_view(['POST'])
def create_stripe_customer_charge(request): 
    """
    Charge Card for Stripe check out

    -----
        {
            user_id:1,
            amount:50,
            currency:USD
        }
      
    """
    try:
        user_id = request.data['user_id'] 
        customer = users.objects.get(id = user_id)
        payment = user_payment_status.objects.get(user_id = user_id)
        currency = request.data['currency']

        stripe.api_key = STRIPE_SECRET_KEY

        stripe_charge = stripe.Charge.create(
                amount = request.data['amount'],
                currency = request.data['currency'],
                customer = customer.stripe_id,
                description="Charge to Send Money",
            )

        if stripe_charge['status'] == "succeeded":

            transaction = helpers.create_transaction(
                user_id = user_id,
                currency = currency, 
                amount = request.data['amount'],
            )

            payment.payment_status = 1
            payment.updated_at= datetime.datetime.today()
            payment.save()

            transaction_data = {

                "id":transaction.id,
                "user_id":transaction.user_id,
                "currency":transaction.currency,
                "amount":transaction.amount
            } 


            success={
                'message':'success',
                "transaction_data":transaction_data,
                'status_code':200
            }
            return Response(success)

        else:
            error={
                'message':'could not charge account',
                'data':[],
                'status_code':500
            }

            return Response(error)  


    except BaseException as e:
        
        error={
            'data':[],
            'message':'error'+ str(e),
            'status_code':500
        }

        return Response(error)  

@api_view(['POST'])
def get_customer_cards(request):
    """
    -----
        {
            stripe_id:cus_asfhajho13
        }
    """
    try:
        stripe.api_key = STRIPE_SECRET_KEY
        card_info = stripe.Customer.retrieve(request.data['stripe_id']).sources.all(limit=1, object='card')
        success={
            'data':card_info,
            'status_code':200,

        }
        return Response(success)

    except BaseException as e:
        error={
            'status_code':500,
            'message':'error' + str(e),
            'data':{
               
            }
        }
        return Response(error)

@api_view(['POST'])
def check_user_payment_status(request):
    """
    -----
        {
            user_id: 1
        }
    """
    try:
        user_id = request.data['user_id']
        payment = user_payment_status.objects.get(user_id = user_id)
        day = datetime.date.today() - payment.updated_at
        if payment.payment_status == 0:
            success={
            'data':[
                {
                    "payment_status": 0,
                }
            ],
            'message':'Not Paid',
            'status_code':200
            }

            return Response(success) 

        elif day.days > 60 and payment.payment_status == 1:
            success={
            'data':[
                {
                    "payment_status": 0,
                }
            ],
            'message':'Not Paid',
            'status_code':200
            }

            return Response(success) 

        elif day.days <= 60 and payment.payment_status == 1:
            success={
            'data':[
                {
                    "payment_status": 1,
                }
            ],
            'message':'Paid',
            'status_code':200
            }

            return Response(success) 
    except BaseException as e:
        error={
            'status_code':500,
            'message':'error' + str(e),
            'data':{
               
            }
        }
        return Response(error)

@api_view(['GET'])
def get_stripe_balance(request): 

    try:
        stripe.api_key = STRIPE_SECRET_KEY

        balance=stripe.Balance.retrieve()
        success={
            "data":balance,
            "message":"success",
            "status_code":200
            } 
        return Response(success) 

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)

@api_view(['POST'])
def stripe_payout(request): 
    """
    Create Stripe Payout

    -----
        {
            amount:50,
            currency:USD,
            accountId_or_cardNo: 3434545
        }
      
    """
    try:
        stripe.api_key = STRIPE_SECRET_KEY

        payout=stripe.Payout.create(
            amount=request.data['amount'],
            currency=request.data['currency'],
            destination=request.data['accountId_or_cardNo'],
        )
        success={
            "data":payout,
            "message":"success",
            "status_code":200
            } 
        return Response(success)   

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)

#get one particelar users transactions
@api_view(['POST'])  
def get_particular_user_transactions(request):

    """
    Update user details
    -----
        {
            user_id:1,
            page:1
            items: 5
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':

            user_id=request.data['user_id']
            page = request.GET.get('page', request.data['page'])
            transact= transactions.objects.filter(user_id=user_id)
            paginator = Paginator(transact, request.data['items'])
            details =[]
            for transaction in paginator.page(page):
                values={
                    'transaction_ref':transaction.transaction_ref,
                    'amount': transaction.amount,
                    'currency': transaction.currency,
                    'created_at': transaction.created_at,
                    'updated_at': transaction.updated_at
                }

                details.append(values)

            data={'data':details,'message':'success','status_code':200}

            return Response(data)
            
    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)

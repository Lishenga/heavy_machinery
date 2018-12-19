from machinery.models import users, logs, transactions
from django.core.serializers import serialize
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
import urllib.request
import datetime
import json
import stripe
import requests
import string
import random

#STRIPE_SECRET_KEY = "sk_test_hQcwVNlTH1MDVLggM1avFWr4"
STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY


def create_log(request, tags, description):
    log = logs(name= "logs",tags="users", description="User Created", created_at = datetime.date.today(), updated_at= datetime.date.today())
    log.save()
    return True

def create_stripe_user(email): 
    user=users.objects.get(email=email)

    if user.stripe_id =="0":
        my_user = stripe.Customer.create(email= email, api_key=STRIPE_SECRET_KEY)
        user = users.objects.get(email=email)
        user.stripe_id = my_user['id']
        user.save()
        success={
            "data":my_user,
            "message":"success",
            "status_code":200
        } 

        return success 

    else:  
        success={ 
            "message":"user already exists",
            "status_code":200
        } 

        return success  

def create_transaction(user_id, amount, currency):
    #status = 1 means paid
    size=10 
    chars=string.ascii_uppercase + string.digits
    newName = ''.join(random.choice(chars) for _ in range(size))
    transaction = transactions(
        transaction_ref = newName, 
        user_id=user_id,
        amount= amount, 
        currency= currency,
        status=1,
        created_at = datetime.date.today(), 
        updated_at= datetime.date.today()
    )
    transaction.save()

    return transaction


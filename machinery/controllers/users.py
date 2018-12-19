from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from machinery.models import users, user_payment_status
from machinery.help import helpers
from django.core.serializers import serialize
from django.contrib.auth.hashers import make_password
from passlib.hash import django_pbkdf2_sha256 as password_handler
import datetime
from django.core.paginator import Paginator
import stripe
from django.conf import settings

STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY

@api_view(['POST'])
def create_user(request):
    """
    Create User
    -----
        {
           
            fname:leon,
            lname:lishenga,
            email:leon@yahoo.com,
            msisdn:254682312,
            password:roshie,
            role: BIDDER or POSTER
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            user = users(
                fname=request.data['fname'],
                lname=request.data['lname'], 
                email=request.data['email'],  
                password=make_password(request.data['password']), 
                role=request.data['role'], 
                status='1', 
                msisdn=request.data['msisdn'],
                stripe_id='0' ,
                card_brand='0', 
                card_last_four='0',  
                trial_end_at='0',
                created_at = datetime.datetime.today(),
                updated_at= datetime.datetime.today()
            )
            user.save()
            payment = user_payment_status(
                user_id= user.id,
                created_at = datetime.datetime.today(),
                updated_at= datetime.datetime.today()
            )
            payment.save()
            helpers.create_stripe_user(request.data['email'])
            #Logging.send_sms(Logging.convert_numbers_to_international(request.data['msisdn'], request.data['country_code']))
            log=helpers.create_log(request= request, tags="users", description="User Created")
            success={
                'message':'success',
                'log':log,
                'status_code':200
            }
            return Response(success)
            
    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{
                'email':request.data['email'],
                'password':request.data['password']
           }
        }
        return Response(error)        



#update existing user    
@api_view(['POST'])
def update_user(request):    
    """
    Update user details
    -----
        {
            id:1,
            fname:leon,
            lname:lishenga,
            email:leon@yahoo.com,
            msisdn:254682312,
            password:roshie,
            role: BIDDER or POSTER
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            user = users.objects.get(id=request.data['id'])
            user.fname = request.data['fname']
            user.lname=request.data['lname']
            user.email=request.data['email']
            user.msisdn=request.data['msisdn'],
            user.role=request.data['role'],
            user.save()
            success={'message':'success','status_code':200}
            return Response(success)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)     


#update existing user    
@api_view(['POST'])
def user_device_uid(request):    
    """
    Update user details
    -----
        {
            user_id:1,
            device_uid:aksdhjashja65546,
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            user = users.objects.get(id=request.data['user_id'])
            user.device_uid = request.data['device_uid'],
            user.save()
            success={'message':'success','status_code':200}
            return Response(success)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)     

#update existing user    
@api_view(['POST'])
def add_user_card(request):    
    """
    Create Stripe Customers Card
    -----
        {
            user_id:1,
            number:424242424242424,
            exp_month:07,
            exp_year:22,
            cvc:494
        }

    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':     
            user_id = request.data['user_id'] 
            card = {
                "number": request.data['number'] ,
                "exp_month": request.data['exp_month'],
                "exp_year": request.data['exp_year'],
                "cvc": request.data['cvc']
            }
            stripe.api_key = STRIPE_SECRET_KEY
            customer = users.objects.get(id=user_id)
            token = stripe.Token.create(card=card, api_key=STRIPE_SECRET_KEY)  
            customer = stripe.Customer.retrieve(customer.stripe_id)
            create_card=customer.sources.create(source= token['id'])
            
            success={
                    "data":create_card,
                    "message":"success",
                    "status_code":200
                } 
            return Response(success)  
    except BaseException as e:

        error={
            'data':[],
            'message':'error'+ str(e),
            'status_code':500
        }

        return Response(error)  
          
       


#update existing user  password   
@api_view(['POST'])
def update_user_password(request):   
    """ 
    Update User Password
    -----
        {
            id:1,
            password:123456
        } 
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            user = users.objects.get(id=request.data['id'])
            user.password = make_password(request.data['password'])
            user.save()
            success={
                'message':'success',
                'status_code':200,
                'data':{}
            }
            return Response(success)

    except BaseException as e:
        
        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)            



#get all existing users
@api_view(['POST'])  
def get_all_users(request):  
    """
    See all users 
    -----
        {
            page:1
            items: 5
        }
    """
    userss= users.objects.all()
    page = request.GET.get('page', request.data['page'])
    paginator = Paginator(userss, request.data['items'])
    details=[]
    for user in paginator.page(page):
        values={
            'id':user.id,
            'fname': user.fname,
            'lname': user.lname,
            'email': user.email,
            'password': user.password,
            'status': user.status,
            'msisdn': user.msisdn,
            'role': user.role,
            'stripe_id': user.stripe_id,
            'card_brand ': user.card_brand,
            'card_last_four': user.card_last_four,
            'trial_end_at': user.trial_end_at,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }

        details.append(values)

    data={
        'data':details,
        'message':'success',
        'status_code':200
        }
    return Response(data)



#get one particelar users details
@api_view(['POST'])  
def get_particular_user_details(request):

    """
    Get particular user details
    -----
        {
            user_id:1,
        }
    """
    if request.method == 'GET':
        success={'message':'method not allowed','status_code':401}
        return Response(success)

    elif request.method == 'POST':

        user_id=request.data['user_id']
        user=users.objects.get(id=user_id)
        details={
            'id':user.id,
            'fname': user.fname,
            'lname': user.lname,
            'email': user.email,
            'password': user.password,
            'status': user.status,
            'msisdn': user.msisdn,
            'role': user.role,
            'stripe_id': user.stripe_id,
            'card_brand ': user.card_brand,
            'card_last_four': user.card_last_four,
            'trial_end_at': user.trial_end_at,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }

        data={'data':details,'message':'success','status_code':200}

        return Response(data)


@api_view(['DELETE'])

def delete_user(request):
    """
    remove user
    -----
        {
            id:1,
        }
    
    """
    try:
        if request.method=='DELETE':
            _id=request.data['id']
            stripe.api_key = STRIPE_SECRET_KEY
            get_user=users.objects.get(id=_id)
            

            if get_user.stripe_id == "0":

                delete=users.objects.filter(id=_id).delete()
                data={
                    "data":"user deleted",
                    "message":delete,
                    "status_code":200
                }
                return Response(data)

            else:
                cu = stripe.Customer.retrieve(get_user.stripe_id)
                delete_stripe = cu.delete()
                delete=users.objects.filter(id=_id).delete()
                data={
                    "data":delete_stripe,
                    "message":'User deleted',
                    "status_code":200
                }
                return Response(data)
        else:
            snippets={
                
                'message':"invalid request",
                "status_code":401
            }
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)
    except:
        try:
            delete=users.objects.filter(id=_id).delete()
            data={
                "data":delete,
                "message":"User deleted",
                "status_code":200
            }
            return Response(data)
        except: 
            data={
                "data":{},
                "message":'user not deleted',
                "status_code":500
            }
            return Response(data)   



@api_view(['POST'])
def get_user_email_login(request):  

    """
    Update user details
    -----
        {
            email:roshie@gmail.com,
            password:roshie,
        }
    """

    try:
        user_id=request.data['email']
        user_input_pass=request.data['password']
        user=users.objects.get(email=user_id)

        if password_handler.verify(user_input_pass, user.password):
            success={
                'data':{
                    'id':user.id,
                    'fname': user.fname,
                    'lname': user.lname,
                    'email': user.email,
                    'password': user.password,
                    'status': user.status,
                    'msisdn': user.msisdn,
                    'stripe_id': user.stripe_id,
                    'role': user.role,
                    'card_brand ': user.card_brand,
                    'card_last_four': user.card_last_four,
                    'trial_end_at': user.trial_end_at,
                    'created_at': user.created_at,
                    'updated_at': user.updated_at
                    },
                'status_code':200,
            }
                
            return Response(success)

        else:
            success={
                'message':'Error',
                'status_code':500
            }
                
            return Response(success)    
    except BaseException as e :
        
        error={
            'status_code':500,
            'message':'error'+str(e),
            'data':{
               
            }
        }
        return Response(error)





from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from machinery.models import user_items_request, category
from machinery.help import helpers
import datetime
import stripe
from django.conf import settings



@api_view(['POST'])
def create_request(request):
    """
    Create User
    -----
        {
            user_id: 1,
            category_id:1
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            requests = user_items_request(
                user_id=request.data['user_id'],
                category_id=request.data['category_id'],
                created_at = datetime.date.today(),
                updated_at= datetime.date.today()
            )
            requests.save()
            success={
                'message':'success',
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


#get all existing users
@api_view(['GET'])  
def get_all_requests(request):  
    requests= user_items_request.objects.all()
    cat = category.objects.all()
    details=[]
    for user in requests:
        for cats in cat:
            values={
                'id':user.id,
                'fname': user.fname,
                'lname': user.lname,
                'email': user.email,
                'password': user.password,
                'status': user.status,
                'msisdn': user.msisdn,
                'stripe_id': user.stripe_id,
                'card_brand ': user.card_brand,
                'card_last_four': user.card_last_four,
                'trial_end_at': user.trial_end_at,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }

            details.append(values)

        paginator = Paginator(details, 10)

    data={'data':paginator,'message':'success','status_code':200}

    return Response(data)



#get one particelar requests details
@api_view(['POST'])  
def get_particular_user_details(request):

    """
    Update user details
    -----
        {
            id:1,
        }
    """
    if request.method == 'GET':
        success={'message':'method not allowed','status_code':401}
        return Response(success)

    elif request.method == 'POST':

        user_id=request.data['id']
        user=Users.objects.get(id=user_id)
        details={
            'id':user.id,
            'fname': user.fname,
            'lname': user.lname,
            'email': user.email,
            'password': user.password,
            'status': user.status,
            'msisdn': user.msisdn,
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
            get_user=Users.objects.get(id=_id)
            

            if get_user.stripe_id == "0":

                delete=Users.objects.filter(id=_id).delete()
                data={
                    "data":delete,
                    "message":"User deleted",
                    "status_code":200
                }
                return Response(data)

            else:
                cu = stripe.Customer.retrieve(get_user.stripe_id)
                delete_stripe = cu.delete()
                delete=Users.objects.filter(id=_id).delete()
                data={
                    "data":delete_stripe,
                    "message":delete,
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
            delete=Users.objects.filter(id=_id).delete()
            data={
                "data":"user deleted",
                "message":delete,
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
        user=Users.objects.get(email=user_id)

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





from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from machinery.models import bids, bids_accept, posts, users, location, category
from machinery.help import pagination
from django.core.paginator import Paginator
import datetime
import stripe
from django.conf import settings



@api_view(['POST'])
def create_bid(request):
    """
    Create Bid
    -----
        {
           
            post_id:1,
            bidder_id:1,
            min_days:4,
            max_days:10,
            price: 200 
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            bid = bids(
                post_id=request.data['post_id'],
                bidder_id=request.data['bidder_id'], 
                min_days=request.data['min_days'],  
                max_days=request.data['max_days'], 
                price=request.data['price'], 
                created_at = datetime.date.today(),
                updated_at= datetime.date.today()
            )
            bid.save()
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
                'post_id':request.data['post_id'],
                'bidder_id':request.data['bidder_id']
           }
        }
        return Response(error)        


@api_view(['POST'])
def accept_bid(request):
    """
    Accept Bid
    -----
        {
            bid_id: 1
            post_id:1,
            bidder_id:1,
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            accept = bids_accept(
                bid_id=request.data['bid_id'],
                post_id=request.data['post_id'], 
                bidder_id=request.data['bidder_id'],  
                created_at = datetime.date.today(),
                updated_at= datetime.date.today()
            )
            bid = bids.objects.get(id=request.data['bid_id'])
            bid.status = 1     
            bid.save()
            post = posts.objects.get(id=request.data['post_id'])
            post.status = 1
            post.save()
            accept.save()
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
                'post_id':request.data['post_id'],
                'bidder_id':request.data['bidder_id']
           }
        }
        return Response(error)   


@api_view(['POST'])
def see_accepted_bids_poster(request):
    """
    See accepted bids for a user 
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
            post = posts.objects.filter(user_id=user_id).filter(status = 1)
            page = request.GET.get('page', request.data['page'])
            paginator = Paginator(post, request.data['items'])
            details=[]
            deta=[]
            detai = []
            da = []
            for poster in paginator.page(page):
                values={
                    'id':poster.id,
                }
                
                details.append(values)

            for cats in details:
                bidding=bids.objects.filter(post_id=cats['id']).get(status = 1)
                val={
                    'bid_id':bidding.id,
                    'post_id': bidding.post_id,
                    'bidder_id': bidding.bidder_id,
                    'max_days': bidding.max_days,
                    'min_days': bidding.min_days,
                    'price': bidding.price,
                    'status': bidding.status,
                    'created_at': bidding.created_at,
                    'updated_at': bidding.updated_at
                }

                deta.append(val)

            for cats in deta:
                post = posts.objects.get(id=cats['post_id'])
                vali={
                    'bid_id':cats['bid_id'],
                    'bid_bidder_id':cats['bidder_id'],
                    'bid_max_days':cats['max_days'],
                    'bid_min_days':cats['min_days'],
                    'bid_price':cats['price'],
                    'bid_status':cats['status'],
                    'bid_updated_at':cats['updated_at'],
                    'post_user_id': post.user_id,
                    'post_name': post.name,
                    'post_description': post.description,
                    'post_max_days': post.max_days,
                    'post_min_days': post.min_days,
                    'post_price': post.price,
                    'post_location_id': post.location_id,
                    'post_category_id':post.category_id,
                }
            
                detai.append(vali)

            for ca in detai:
                user=users.objects.get(id=ca['bid_bidder_id'])
                userss=users.objects.get(id=ca['post_user_id'])
                loc = location.objects.get(id = ca['post_location_id'])
                cate = category.objects.get(category_id=ca['post_category_id'])
                va={
                    'bid_id':ca['bid_id'],
                    'poster_name':userss.fname+' '+userss.lname,
                    'bidder_name':user.fname+' '+user.lname,
                    'bid_bidder_id':ca['bid_bidder_id'],
                    'bid_max_days':ca['bid_max_days'],
                    'bids_min_days':ca['bid_min_days'],
                    'bid_price':ca['bid_price'],
                    'bid_status':ca['bid_status'],
                    'bid_updated_at':ca['bid_updated_at'],
                    'post_user_id': ca['post_user_id'],
                    'post_name': ca['post_name'],
                    'description': ca['post_description'],
                    'post_max_days': ca['post_max_days'],
                    'post_min_days': ca['post_min_days'],
                    'post_price': ca['post_price'],
                    'post_location_county': loc.county,
                    'post_loaction_ward': loc.ward,
                    'post_category_name':cate.name,
                }

                da.append(va)

            data={
                'data':da,
                'message':'success',
                'status_code':200
                }
            return Response(data)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)

@api_view(['POST'])
def see_specific_accepted_bid_poster(request):
    """
    See specific accepted bid for a user or poster
    -----
        {
            post_id: 1
            user_id:1,
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':

            user_id=request.data['user_id']
            post_id=request.data['post_id']
            post = posts.objects.filter(user_id=user_id).filter(status = 1).get(id=post_id)
            details=[]
            deta=[]
            detai=[]
            da=[]
            values={
                    'id':post.id,
                }

            details.append(values)

            for cats in details:
                bidding=bids.objects.filter(post_id=cats['id']).get(status = 1)
                val={
                    'id':bidding.id,
                    'post_id': bidding.post_id,
                    'bidder_id': bidding.bidder_id,
                    'max_days': bidding.max_days,
                    'min_days': bidding.min_days,
                    'price': bidding.price,
                    'status': bidding.status,
                    'created_at': bidding.created_at,
                    'updated_at': bidding.updated_at
                }

                deta.append(val) 

            for cas in deta:
                post = posts.objects.get(id=cas['post_id'])
                vali={
                    'bid_id':cas['id'],
                    'bid_bidder_id':cas['bidder_id'],
                    'bid_max_days':cas['max_days'],
                    'bid_min_days':cas['min_days'],
                    'bid_price':cas['price'],
                    'bid_status':cas['status'],
                    'bid_updated_at':cas['updated_at'],
                    'post_user_id': post.user_id,
                    'post_name': post.name,
                    'post_description': post.description,
                    'post_max_days': post.max_days,
                    'post_min_days': post.min_days,
                    'post_price': post.price,
                    'post_location_id': post.location_id,
                    'post_category_id':post.category_id,
                }
            
                detai.append(vali)

            for ca in detai:
                user=users.objects.get(id=ca['bid_bidder_id'])
                userss=users.objects.get(id=ca['post_user_id'])
                loc = location.objects.get(id = ca['post_location_id'])
                cate = category.objects.get(category_id=ca['post_category_id'])
                va={
                    'bid_id':ca['bid_id'],
                    'poster_name':userss.fname+' '+userss.lname,
                    'bidder_name':user.fname+' '+user.lname,
                    'bid_bidder_id':ca['bid_bidder_id'],
                    'bid_max_days':ca['bid_max_days'],
                    'bids_min_days':ca['bid_min_days'],
                    'bid_price':ca['bid_price'],
                    'bid_status':ca['bid_status'],
                    'bid_updated_at':ca['bid_updated_at'],
                    'post_user_id': ca['post_user_id'],
                    'post_name': ca['post_name'],
                    'description': ca['post_description'],
                    'post_max_days': ca['post_max_days'],
                    'post_min_days': ca['post_min_days'],
                    'post_price': ca['post_price'],
                    'post_location_county': loc.county,
                    'post_loaction_ward': loc.ward,
                    'post_category_name':cate.name,
                }

                da.append(va)
                            
            data={
                'data':da,
                'message':'success',
                'status_code':200
                }
            return Response(data)
    
    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)

@api_view(['POST'])
def see_accepted_bids_bidder(request):
    """
    See accepted bids for a bidder 
    -----
        {
            bidder_id:1,
            page: 1,
            items: 5
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':

            bidder_id=request.data['bidder_id']
            page = request.GET.get('page', request.data['page'])
            details =[]
            deta=[]
            da=[]
            bidding=bids.objects.filter(bidder_id=bidder_id).filter(status = 1)
            paginator = Paginator(bidding, request.data['items'])
            for bidder in paginator.page(page):  
                values={
                    'id':bidder.id,
                    'post_id': bidder.post_id,
                    'bidder_id': bidder.bidder_id,
                    'max_days': bidder.max_days,
                    'min_days': bidder.min_days,
                    'price': bidder.price,
                    'status': bidder.status,
                    'created_at': bidder.created_at,
                    'updated_at': bidder.updated_at
                }

                details.append(values)
            
            for cats in details:
                post = posts.objects.get(id=cats['post_id'])
                val={
                    'bid_id':cats['id'],
                    'bid_bidder_id':cats['bidder_id'],
                    'bid_max_days':cats['max_days'],
                    'bid_min_days':cats['min_days'],
                    'bid_price':cats['price'],
                    'bid_status':cats['status'],
                    'bid_updated_at':cats['updated_at'],
                    'post_user_id': post.user_id,
                    'post_name': post.name,
                    'post_description': post.description,
                    'post_max_days': post.max_days,
                    'post_min_days': post.min_days,
                    'post_price': post.price,
                    'post_location_id': post.location_id,
                    'post_category_id':post.category_id,
                }
            
                deta.append(val)

            for ca in deta:
                user=users.objects.get(id=ca['bid_bidder_id'])
                userss=users.objects.get(id=ca['post_user_id'])
                loc = location.objects.get(id = ca['post_location_id'])
                cate = category.objects.get(category_id=ca['post_category_id'])
                va={
                    'bid_id':ca['bid_id'],
                    'poster_name':userss.fname+' '+userss.lname,
                    'bidder_name':user.fname+' '+user.lname,
                    'bid_bidder_id':ca['bid_bidder_id'],
                    'bid_max_days':ca['bid_max_days'],
                    'bids_min_days':ca['bid_min_days'],
                    'bid_price':ca['bid_price'],
                    'bid_status':ca['bid_status'],
                    'bid_updated_at':ca['bid_updated_at'],
                    'post_user_id': ca['post_user_id'],
                    'post_name': ca['post_name'],
                    'description': ca['post_description'],
                    'post_max_days': ca['post_max_days'],
                    'post_min_days': ca['post_min_days'],
                    'post_price': ca['post_price'],
                    'post_location_county': loc.county,
                    'post_loaction_ward': loc.ward,
                    'post_category_name':cate.name,
                }

                da.append(va)

            data={
                'data':da,
                'message':'success',
                'status_code':200
                }
            return Response(data)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)


@api_view(['POST'])  
def get_all_bids_accepted(request):  
    """
    Get all accepted bids 
    -----
        {
            page: 1,
            items: 5
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':
            details=[]
            deta=[]
            da=[]
            bidd = bids.objects.filter(status = 1) 
            page = request.GET.get('page', request.data['page'])
            paginator = Paginator(bidd, request.data['items'])
            for bidding in paginator.page(page):
                val={
                    'id':bidding.id,
                    'post_id': bidding.post_id,
                    'bidder_id': bidding.bidder_id,
                    'max_days': bidding.max_days,
                    'min_days': bidding.min_days,
                    'price': bidding.price,
                    'status': bidding.status,
                    'created_at': bidding.created_at,
                    'updated_at': bidding.updated_at
                }

                details.append(val)

            for cats in details:
                post = posts.objects.get(id=cats['post_id'])
                val={
                    'bid_id':cats['id'],
                    'bid_bidder_id':cats['bidder_id'],
                    'bid_max_days':cats['max_days'],
                    'bid_min_days':cats['min_days'],
                    'bid_price':cats['price'],
                    'bid_status':cats['status'],
                    'bid_updated_at':cats['updated_at'],
                    'post_user_id': post.user_id,
                    'post_name': post.name,
                    'post_description': post.description,
                    'post_max_days': post.max_days,
                    'post_min_days': post.min_days,
                    'post_price': post.price,
                    'post_location_id': post.location_id,
                    'post_category_id':post.category_id,
                }
            
                deta.append(val)

            for ca in deta:
                user=users.objects.get(id=ca['bid_bidder_id'])
                userss=users.objects.get(id=ca['post_user_id'])
                loc = location.objects.get(id = ca['post_location_id'])
                cate = category.objects.get(category_id=ca['post_category_id'])
                va={
                    'bid_id':ca['bid_id'],
                    'poster_name':userss.fname+' '+userss.lname,
                    'bidder_name':user.fname+' '+user.lname,
                    'bid_bidder_id':ca['bid_bidder_id'],
                    'bid_max_days':ca['bid_max_days'],
                    'bids_min_days':ca['bid_min_days'],
                    'bid_price':ca['bid_price'],
                    'bid_status':ca['bid_status'],
                    'bid_updated_at':ca['bid_updated_at'],
                    'post_user_id': ca['post_user_id'],
                    'post_name': ca['post_name'],
                    'description': ca['post_description'],
                    'post_max_days': ca['post_max_days'],
                    'post_min_days': ca['post_min_days'],
                    'post_price': ca['post_price'],
                    'post_location_county': loc.county,
                    'post_loaction_ward': loc.ward,
                    'post_category_name':cate.name,
                }

                da.append(va)

            data={
                'data':da,
                'message':'success',
                'status_code':200
                }
            return Response(data)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)


@api_view(['POST'])
def see_specific_accepted_bid_bidder(request):
    """
    See specific accepted bid for a bidder 
    -----
        {
            bidder_id:1,
            bid_id: 1
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':

            bidder_id=request.data['bidder_id']
            bid_id=request.data['bid_id']
            bidding=bids.objects.filter(bidder_id=bidder_id).filter(status = 1).get(id=bid_id)
            details=[]
            deta=[]
            da=[]
            values={
                'id':bidding.id,
                'post_id': bidding.post_id,
                'bidder_id': bidding.bidder_id,
                'max_days': bidding.max_days,
                'min_days': bidding.min_days,
                'price': bidding.price,
                'status': bidding.status,
                'created_at': bidding.created_at,
                'updated_at': bidding.updated_at
            }

            details.append(values)

            for cats in details:
                post = posts.objects.get(id=cats['post_id'])
                val={
                    'bid_id':cats['id'],
                    'bid_bidder_id':cats['bidder_id'],
                    'bid_max_days':cats['max_days'],
                    'bid_min_days':cats['min_days'],
                    'bid_price':cats['price'],
                    'bid_status':cats['status'],
                    'bid_updated_at':cats['updated_at'],
                    'post_user_id': post.user_id,
                    'post_name': post.name,
                    'post_description': post.description,
                    'post_max_days': post.max_days,
                    'post_min_days': post.min_days,
                    'post_price': post.price,
                    'post_location_id': post.location_id,
                    'post_category_id':post.category_id,
                }
            
                deta.append(val)

            for ca in deta:
                user=users.objects.get(id=ca['bid_bidder_id'])
                userss=users.objects.get(id=ca['post_user_id'])
                loc = location.objects.get(id = ca['post_location_id'])
                cate = category.objects.get(category_id=ca['post_category_id'])
                va={
                    'bid_id':ca['bid_id'],
                    'poster_name':userss.fname+' '+userss.lname,
                    'bidder_name':user.fname+' '+user.lname,
                    'bid_bidder_id':ca['bid_bidder_id'],
                    'bid_max_days':ca['bid_max_days'],
                    'bids_min_days':ca['bid_min_days'],
                    'bid_price':ca['bid_price'],
                    'bid_status':ca['bid_status'],
                    'bid_updated_at':ca['bid_updated_at'],
                    'post_user_id': ca['post_user_id'],
                    'post_name': ca['post_name'],
                    'description': ca['post_description'],
                    'post_max_days': ca['post_max_days'],
                    'post_min_days': ca['post_min_days'],
                    'post_price': ca['post_price'],
                    'post_location_county': loc.county,
                    'post_loaction_ward': loc.ward,
                    'post_category_name':cate.name,
                }

                da.append(va)

            data={
                'data':da,
                'message':'success',
                'status_code':200
                }
            return Response(data)
    
    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)

#update existing bid    
@api_view(['POST'])
def update_bid(request):    
    """
    Update user bid
    -----
        {
            id:1,
            post_id:1,
            bidder_id:1,
            min_days:4,
            max_days:10,
            price: 200 
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            bid = bids.objects.get(id=request.data['id'])
            bid.post_id = request.data['post_id']
            bid.bidder_id=request.data['bidder_id']
            bid.min_days=request.data['min_days'],
            bid.max_days=request.data['max_days'],
            bid.price=request.data['price'],
            bid.updated_at= datetime.date.today()
            bid.save()
            success={'message':'success','status_code':200}
            return Response(success)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)


#get all existing bids
@api_view(['POST'])  
def get_all_bids(request):  
    """
    Get all existing bids by page number
    -----
        {
            page: 1,
            items: 5
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':

            bid= bids.objects.all().order_by('-updated_at')
            page = request.GET.get('page', request.data['page'])
            paginator = Paginator(bid, request.data['items'])
            details=[]
            deta=[]
            da=[]
            for bidder in paginator.page(page):
                values={
                    'id':bidder.id,
                    'post_id': bidder.post_id,
                    'bidder_id': bidder.bidder_id,
                    'max_days': bidder.max_days,
                    'min_days': bidder.min_days,
                    'price': bidder.price,
                    'status': bidder.status,
                    'created_at': bidder.created_at,
                    'updated_at': bidder.updated_at
                }

                details.append(values)
            
            for cats in details:
                post = posts.objects.get(id=cats['post_id'])
                val={
                    'bid_id':cats['id'],
                    'bid_bidder_id':cats['bidder_id'],
                    'bid_max_days':cats['max_days'],
                    'bid_min_days':cats['min_days'],
                    'bid_price':cats['price'],
                    'bid_status':cats['status'],
                    'bid_updated_at':cats['updated_at'],
                    'post_user_id': post.user_id,
                    'post_name': post.name,
                    'post_description': post.description,
                    'post_max_days': post.max_days,
                    'post_min_days': post.min_days,
                    'post_price': post.price,
                    'post_location_id': post.location_id,
                    'post_category_id':post.category_id,
                }
            
            deta.append(val)

            for ca in deta:
                user=users.objects.get(id=ca['bid_bidder_id'])
                userss=users.objects.get(id=ca['post_user_id'])
                loc = location.objects.get(id = ca['post_location_id'])
                cate = category.objects.get(category_id=ca['post_category_id'])
                va={
                    'bid_id':ca['bid_id'],
                    'poster_name':userss.fname+' '+userss.lname,
                    'bidder_name':user.fname+' '+user.lname,
                    'bid_bidder_id':ca['bid_bidder_id'],
                    'bid_max_days':ca['bid_max_days'],
                    'bids_min_days':ca['bid_min_days'],
                    'bid_price':ca['bid_price'],
                    'bid_status':ca['bid_status'],
                    'bid_updated_at':ca['bid_updated_at'],
                    'post_user_id': ca['post_user_id'],
                    'post_name': ca['post_name'],
                    'description': ca['post_description'],
                    'post_max_days': ca['post_max_days'],
                    'post_min_days': ca['post_min_days'],
                    'post_price': ca['post_price'],
                    'post_location_county': loc.county,
                    'post_loaction_ward': loc.ward,
                    'post_category_name':cate.name,
                }

                da.append(va)

            data={
                'data':da,
                'message':'success',
                'status_code':200,
            }

            return Response(data)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)



#get one particular bids for bidder
@api_view(['POST'])  
def get_particular_user_bids(request):

    """
    Get particular user's bids
    -----
        {
            bidder_id:1,
            page: 1,
            items: 5
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':

            bidder_id=request.data['bidder_id']
            bid=bids.objects.filter(bidder_id=bidder_id)
            page = request.GET.get('page', request.data['page'])
            paginator = Paginator(bid, request.data['items'])
            details=[]
            deta=[]
            da=[]
            for bidder in paginator.page(page):
                values={
                    'id':bidder.id,
                    'post_id': bidder.post_id,
                    'bidder_id': bidder.bidder_id,
                    'max_days': bidder.max_days,
                    'min_days': bidder.min_days,
                    'price': bidder.price,
                    'status': bidder.status,
                    'created_at': bidder.created_at,
                    'updated_at': bidder.updated_at
                }

                details.append(values)

            for cats in details:
                post = posts.objects.get(id=cats['post_id'])
                val={
                    'bid_id':cats['id'],
                    'bid_bidder_id':cats['bidder_id'],
                    'bid_max_days':cats['max_days'],
                    'bid_min_days':cats['min_days'],
                    'bid_price':cats['price'],
                    'bid_status':cats['status'],
                    'bid_updated_at':cats['updated_at'],
                    'post_user_id': post.user_id,
                    'post_name': post.name,
                    'post_description': post.description,
                    'post_max_days': post.max_days,
                    'post_min_days': post.min_days,
                    'post_price': post.price,
                    'post_location_id': post.location_id,
                    'post_category_id':post.category_id,
                }
                
                deta.append(val)
            
            for ca in deta:
                user=users.objects.get(id=ca['bid_bidder_id'])
                userss=users.objects.get(id=ca['post_user_id'])
                loc = location.objects.get(id = ca['post_location_id'])
                cate = category.objects.get(category_id=ca['post_category_id'])
                va={
                    'bid_id':ca['bid_id'],
                    'poster_name':userss.fname+' '+userss.lname,
                    'bidder_name':user.fname+' '+user.lname,
                    'bid_bidder_id':ca['bid_bidder_id'],
                    'bid_max_days':ca['bid_max_days'],
                    'bids_min_days':ca['bid_min_days'],
                    'bid_price':ca['bid_price'],
                    'bid_status':ca['bid_status'],
                    'bid_updated_at':ca['bid_updated_at'],
                    'post_user_id': ca['post_user_id'],
                    'post_name': ca['post_name'],
                    'description': ca['post_description'],
                    'post_max_days': ca['post_max_days'],
                    'post_min_days': ca['post_min_days'],
                    'post_price': ca['post_price'],
                    'post_location_county': loc.county,
                    'post_loaction_ward': loc.ward,
                    'post_category_name':cate.name,
                }

                da.append(va)

            data={
                'data':da,
                'message':'success',
                'status_code':200
                }
            return Response(data)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)

#get one particular bid
@api_view(['POST'])  
def get_particular_bid(request):

    """
    Get particular user's specific bid
    -----
        {
            id: 1
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':
        
            id=request.data['id']
            bid=bids.objects.get(id=id)
            details=[]
            deta=[]
            da=[]
            values={
                'id':bid.id,
                'bidder_id': bid.bidder_id,
                'post_id': bid.post_id,
                'max_days': bid.max_days,
                'min_days': bid.max_days,
                'price': bid.price,
                'status': bid.status,
                'created_at': bid.created_at,
                'updated_at': bid.updated_at
            }

            details.append(values)

            for cats in details:
                post = posts.objects.get(id=cats['post_id'])
                val={
                    'bid_id':cats['id'],
                    'bid_bidder_id':cats['bidder_id'],
                    'bid_max_days':cats['max_days'],
                    'bid_min_days':cats['min_days'],
                    'bid_price':cats['price'],
                    'bid_status':cats['status'],
                    'bid_updated_at':cats['updated_at'],
                    'post_user_id': post.user_id,
                    'post_name': post.name,
                    'post_description': post.description,
                    'post_max_days': post.max_days,
                    'post_min_days': post.min_days,
                    'post_price': post.price,
                    'post_location_id': post.location_id,
                    'post_category_id':post.category_id,
                }
                
                deta.append(val)

            for ca in deta:
                user=users.objects.get(id=ca['bid_bidder_id'])
                userss=users.objects.get(id=ca['post_user_id'])
                loc = location.objects.get(id = ca['post_location_id'])
                cate = category.objects.get(category_id=ca['post_category_id'])
                va={
                    'bid_id':ca['bid_id'],
                    'poster_name':userss.fname+' '+userss.lname,
                    'bidder_name':user.fname+' '+user.lname,
                    'bid_bidder_id':ca['bid_bidder_id'],
                    'bid_max_days':ca['bid_max_days'],
                    'bids_min_days':ca['bid_min_days'],
                    'bid_price':ca['bid_price'],
                    'bid_status':ca['bid_status'],
                    'bid_updated_at':ca['bid_updated_at'],
                    'post_user_id': ca['post_user_id'],
                    'post_name': ca['post_name'],
                    'description': ca['post_description'],
                    'post_max_days': ca['post_max_days'],
                    'post_min_days': ca['post_min_days'],
                    'post_price': ca['post_price'],
                    'post_location_county': loc.county,
                    'post_loaction_ward': loc.ward,
                    'post_category_name':cate.name,
                }

                da.append(va)

            data={
                'data':da,
                'message':'success',
                'status_code':200
                }
            return Response(data)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)


#get one particular bids for a post
@api_view(['POST'])  
def get_particular_posts_bids(request):

    """
    Get particular post's specific bids
    -----
        {
            post_id:1,
            page: 1,
            items: 5
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':

            post_id=request.data['post_id']
            bid=bids.objects.filter(post_id=post_id)
            page = request.GET.get('page', request.data['page'])
            paginator = Paginator(bid, request.data['items'])
            details=[]
            deta=[]
            da=[]
            for bidder in paginator.page(page):
                values={
                    'id':bidder.id,
                    'post_id': bidder.post_id,
                    'bidder_id': bidder.bidder_id,
                    'max_days': bidder.max_days,
                    'min_days': bidder.min_days,
                    'price': bidder.price,
                    'status': bidder.status,
                    'created_at': bidder.created_at,
                    'updated_at': bidder.updated_at
                }

                details.append(values)

            for cats in details:
                post = posts.objects.get(id=cats['post_id'])
                val={
                    'bid_id':cats['id'],
                    'bid_bidder_id':cats['bidder_id'],
                    'bid_max_days':cats['max_days'],
                    'bid_min_days':cats['min_days'],
                    'bid_price':cats['price'],
                    'bid_status':cats['status'],
                    'bid_updated_at':cats['updated_at'],
                    'post_user_id': post.user_id,
                    'post_name': post.name,
                    'post_description': post.description,
                    'post_max_days': post.max_days,
                    'post_min_days': post.min_days,
                    'post_price': post.price,
                    'post_location_id': post.location_id,
                    'post_category_id':post.category_id,
                }
            
            deta.append(val)

            for ca in deta:
                user=users.objects.get(id=ca['bid_bidder_id'])
                userss=users.objects.get(id=ca['post_user_id'])
                loc = location.objects.get(id = ca['post_location_id'])
                cate = category.objects.get(category_id=ca['post_category_id'])
                va={
                    'bid_id':ca['bid_id'],
                    'poster_name':userss.fname+' '+userss.lname,
                    'bidder_name':user.fname+' '+user.lname,
                    'bid_bidder_id':ca['bid_bidder_id'],
                    'bid_max_days':ca['bid_max_days'],
                    'bids_min_days':ca['bid_min_days'],
                    'bid_price':ca['bid_price'],
                    'bid_status':ca['bid_status'],
                    'bid_updated_at':ca['bid_updated_at'],
                    'post_user_id': ca['post_user_id'],
                    'post_name': ca['post_name'],
                    'description': ca['post_description'],
                    'post_max_days': ca['post_max_days'],
                    'post_min_days': ca['post_min_days'],
                    'post_price': ca['post_price'],
                    'post_location_county': loc.county,
                    'post_loaction_ward': loc.ward,
                    'post_category_name':cate.name,
                }

                da.append(va)

            data={
                'data':da,
                'message':'success',
                'status_code':200
            }
            
            return Response(data)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)

@api_view(['DELETE'])
def delete_bid(request):
    """
    remove bid
    -----
        {
            id:1,
        }
    
    """
    try:
        if request.method=='DELETE':
            _id=request.data['id']

            delete=bids.objects.filter(id=_id).delete()
            data={
                "data":delete,
                "message":"bid deleted",
                "status_code":200
            }
            return Response(data)

        else:
            snippets={
                
                'message':"method not allowed",
                "status_code":400
            }
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)
    except:
        data={
            "data":{},
            "message":'category not deleted',
            "status_code":500
        }
        return Response(data)   




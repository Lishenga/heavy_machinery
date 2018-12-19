from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from machinery.models import posts, location, category
from django.db.models import F
import datetime
from django.core.paginator import Paginator
import stripe
from django.conf import settings



@api_view(['POST'])
def create_post(request):
    """
    Create Post
    -----
        {
           
            user_id:1,
            name:lishenga,
            description:dsdvsdvjkldv,
            min_days:4,
            max_days:10,
            price: 200,
            location_id: 1
            category_id: 1
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            post = posts(
                user_id=request.data['user_id'],
                name=request.data['name'],
                description=request.data['description'], 
                min_days=request.data['min_days'],  
                max_days=request.data['max_days'], 
                price=request.data['price'], 
                location_id=request.data['location_id'],
                category_id=request.data['category_id'],
                created_at = datetime.date.today(),
                updated_at= datetime.date.today()
            )
            post.save()
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
                'user_id':request.data['user_id'],
                'name':request.data['name']
           }
        }
        return Response(error)        



#update existing post    
@api_view(['POST'])
def update_post(request):    
    """
    Update user post
    -----
        {
            id:1,
            user_id:1,
            name:lishenga,
            description:dsdvsdvjkldv,
            min_days:4,
            max_days:10,
            price: 200,
            location_id: 1
            category_id: 1
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            post = posts.objects.get(id=request.data['id'])
            post.user_id = request.data['user_id']
            post.name=request.data['name']
            post.description=request.data['description']
            post.min_days=request.data['min_days'],
            post.max_days=request.data['max_days'],
            post.price=request.data['price'],
            post.location_id=request.data['location_id'],
            post.category_id=request.data['category_id'],
            post.updated_at= datetime.date.today()
            post.save()
            success={'message':'success','status_code':200}
            return Response(success)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)


#get all existing post
@api_view(['POST'])  
def get_all_posts(request):  
    """
    See all Posts
    -----
        {
            page:1
            items: 5
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':

            post= posts.objects.filter(status = 0)

            page = request.GET.get('page', request.data['page'])
            paginator = Paginator(post, request.data['items'])

            details=[]
            deta=[]
            for poster in paginator.page(page):
                values={
                        'id':poster.id,
                        'user_id': poster.user_id,
                        'name': poster.name,
                        'description': poster.description,
                        'max_days': poster.max_days,
                        'min_days': poster.min_days,
                        'price': poster.price,
                        'location_id': poster.location_id,
                        'category_id':poster.category_id,
                        'status': poster.status,
                        'created_at': poster.created_at,
                        'updated_at': poster.updated_at
                    }

                details.append(values)

            for cats in details:
                loc = location.objects.get(id=cats['location_id'])
                cat = category.objects.get(category_id=cats['category_id'])
                val={
                    'id':cats['id'],
                    'user_id': cats['user_id'],
                    'name': cats['name'],
                    'description': cats['description'],
                    'max_days': cats['max_days'],
                    'min_days': cats['min_days'],
                    'price': cats['price'],
                    'status': cats['status'],
                    'loaction_id': cats['location_id'],
                    'region': loc.region,
                    'county': loc.county,
                    'province': loc.province,
                    'category_name':cat.name,
                    'category_description':cat.description,
                    'ward_or_town': loc.ward,
                    'created_at': cats['created_at'],
                    'updated_at': cats['updated_at']
                }

                deta.append(val)

                #paginator = Paginator(details, 10)

            data={'data':deta,'message':'success','status_code':200}
            
            return Response(data)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)


#get one particelar users details
@api_view(['POST'])  
def get_particular_user_posts(request):

    """
    Get particular user's posts
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
            post=posts.objects.filter(user_id=user_id)

            page = request.GET.get('page', request.data['page'])
            paginator = Paginator(post, request.data['items'])

            details=[]
            deta=[]
            for poster in paginator.page(page):
                values={
                        'id':poster.id,
                        'user_id': poster.user_id,
                        'name': poster.name,
                        'description': poster.description,
                        'max_days': poster.max_days,
                        'min_days': poster.min_days,
                        'price': poster.price,
                        'location_id': poster.location_id,
                        'category_id':poster.category_id,
                        'status': poster.status,
                        'created_at': poster.created_at,
                        'updated_at': poster.updated_at
                    }

                details.append(values)

            
            for cats in details:
                loc = location.objects.get(id=cats['location_id'])
                cat = category.objects.get(category_id=cats['category_id'])
                val={
                    'id':cats['id'],
                    'user_id': cats['user_id'],
                    'name': cats['name'],
                    'description': cats['description'],
                    'max_days': cats['max_days'],
                    'min_days': cats['min_days'],
                    'price': cats['price'],
                    'status': cats['status'],
                    'region': loc.region,
                    'county': loc.county,
                    'province': loc.province,
                    'category_name':cat.name,
                    'category_description':cat.description,
                    'ward_or_town': loc.ward,
                    'created_at': cats['created_at'],
                    'updated_at': cats['updated_at']
                }

                deta.append(val)  
            data={
                'data':deta,
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


#get one particelar users details
@api_view(['POST'])  
def get_particular_post(request):

    """
    Get particular user's specific post
    -----
        {
            id: 1,
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':
            id=request.data['id']
            poster=posts.objects.get(id=id)

            details=[]
            deta=[]
            values={
                    'id':poster.id,
                    'user_id': poster.user_id,
                    'name': poster.name,
                    'description': poster.description,
                    'max_days': poster.max_days,
                    'min_days': poster.min_days,
                    'price': poster.price,
                    'location_id': poster.location_id,
                    'category_id':poster.category_id,
                    'status': poster.status,
                    'created_at': poster.created_at,
                    'updated_at': poster.updated_at
                }

            details.append(values)

            
            for cats in details:
                loc = location.objects.get(id=cats['location_id'])
                cat = category.objects.get(category_id=cats['category_id'])
                val={
                    'id':cats['id'],
                    'user_id': cats['user_id'],
                    'name': cats['name'],
                    'description': cats['description'],
                    'max_days': cats['max_days'],
                    'min_days': cats['min_days'],
                    'price': cats['price'],
                    'status': cats['status'],
                    'region': loc.region,
                    'county': loc.county,
                    'province': loc.province,
                    'category_name':cat.name,
                    'category_description':cat.description,
                    'ward_or_town': loc.ward,
                    'created_at': cats['created_at'],
                    'updated_at': cats['updated_at']
                }

                deta.append(val)  
            data={
                'data':deta,
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


#get posts for accepted bids
@api_view(['POST'])  
def get_posts_for_accepted_bids(request):

    """
    Get particular user's posts for accepted bids
    -----
        {
            user_id:1,
            page:1
            items:10
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':

            user_id=request.data['user_id']
            post=posts.objects.filter(status=1).filter(user_id=user_id)

            page = request.GET.get('page', request.data['page'])
            paginator = Paginator(post, request.data['items'])

            details=[]
            deta=[]
            for poster in paginator.page(page):
                values={
                        'id':poster.id,
                        'user_id': poster.user_id,
                        'name': poster.name,
                        'description': poster.description,
                        'max_days': poster.max_days,
                        'min_days': poster.min_days,
                        'price': poster.price,
                        'location_id': poster.location_id,
                        'category_id':poster.category_id,
                        'status': poster.status,
                        'created_at': poster.created_at,
                        'updated_at': poster.updated_at
                    }

                details.append(values)

            
            for cats in details:
                loc = location.objects.get(id=cats['location_id'])
                cat = category.objects.get(category_id=cats['category_id'])
                val={
                    'id':cats['id'],
                    'user_id': cats['user_id'],
                    'name': cats['name'],
                    'description': cats['description'],
                    'max_days': cats['max_days'],
                    'min_days': cats['min_days'],
                    'price': cats['price'],
                    'status': cats['status'],
                    'region': loc.region,
                    'county': loc.county,
                    'province': loc.province,
                    'category_name':cat.name,
                    'category_description':cat.description,
                    'ward_or_town': loc.ward,
                    'created_at': cats['created_at'],
                    'updated_at': cats['updated_at']
                }

                deta.append(val)  
            data={
                'data':deta,
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
def delete_post(request):
    """
    remove post
    -----
        {
            id:1,
        }
    
    """
    try:
        if request.method=='DELETE':
            _id=request.data['id']

            delete=posts.objects.filter(id=_id).delete()
            data={
                "data":delete,
                "message":"Post deleted",
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



#Search for posts based on location and category
@api_view(['POST'])  
def search_for_posts(request):

    """
    Search for posts based on location and category..Note: pages and items can't be null but other fields can be null
    -----
        {
            category_id:1,
            location_region: Changamwe
            location_county: Mombasa
            location_ward_or_town: Port Reltz
            page: 1
            items: 10
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':

            #all fields are provided

            if request.data['category_id'] is not None and request.data['category_id'] != '':
                if request.data['location_region'] is not None and request.data['location_region'] != '':
                    if request.data['location_county'] is not None and request.data['location_county'] != '':
                        if request.data['location_ward_or_town'] is not None and request.data['location_ward_or_town'] != '':

                            category_id=request.data['category_id']
                            location_region = request.data['location_region'] 
                            location_county = request.data['location_county']
                            location_ward_or_town = request.data['location_ward_or_town']  

                            loca =location.objects.filter(region=location_region).filter(county= location_county).get(ward = location_ward_or_town)
                            cat = category.objects.get(category_id=category_id)
                            post=posts.objects.filter(status=0).filter(category_id=category_id).filter(location_id = loca.id)

                            page = request.GET.get('page', request.data['page'])
                            paginator = Paginator(post, request.data['items'])
                            details=[]

                            for poster in paginator.page(page):
                                values={
                                    'id':poster.id,
                                    'user_id': poster.user_id,
                                    'name': poster.name,
                                    'description': poster.description,
                                    'max_days': poster.max_days,
                                    'min_days': poster.min_days,
                                    'price': poster.price,
                                    'location_id': poster.location_id,
                                    'category_id':poster.category_id,
                                    'status': poster.status,
                                    'created_at': poster.created_at,
                                    'updated_at': poster.updated_at,
                                    'region':loca.region,
                                    'province':loca.province,
                                    'category_name':cat.name,
                                    'category_description':cat.description,
                                    'county':loca.county,
                                    'ward':loca.ward
                                }

                                details.append(values)

                            data={
                                'data':details,
                                'message':'success',
                                'status_code':200
                                }

                            return Response(data)

                #Location_region only provided, other fields empty or none

            elif request.data['location_region'] is not None and request.data['location_region'] != '':
                if request.data['category_id'] is None or request.data['category_id'] == '':
                    if request.data['location_county'] is None or request.data['location_county'] == '':
                        if request.data['location_ward_or_town'] is None or request.data['location_ward_or_town'] == '':

                            location_region = request.data['location_region'] 

                            loca = location.objects.filter(region=location_region)

                            page = request.GET.get('page', request.data['page'])
                            paginator = Paginator(loca, request.data['items'])
                            details=[]
                            deta = []
                            dat=[]
                            for loci in paginator.page(page):
                                values={
                                    'id':loci.id,
                                    'ward_or_town': loci.ward,
                                    'region': loci.region,
                                    'county': loci.county,
                                    'province': loci.province,
                                    'created_at': loci.created_at,
                                    'updated_at': loci.updated_at
                                }

                                details.append(values)

                            for cats in details:
                                poster=posts.objects.filter(location_id = cats['id'])
                                for post in poster:
                                    val={
                                        'id':post.id,
                                        'user_id': post.user_id,
                                        'name': post.name,
                                        'description': post.description,
                                        'max_days': post.max_days,
                                        'min_days': post.min_days,
                                        'category_id':post.category_id,
                                        'price': post.price,
                                        'status': post.status,
                                        'region': cats['region'],
                                        'county': cats['county'],
                                        'province': cats['province'],
                                        'ward_or_town': cats['ward_or_town'],
                                        'created_at': post.created_at,
                                        'updated_at': post.updated_at
                                    }

                                    deta.append(val)

                            for cata in deta:
                                cat = category.objects.filter(category_id = cata['category_id'])
                                for ca in cat:
                                    va={
                                    'id':cata['id'],
                                    'user_id': cata['user_id'],
                                    'name': cata['name'],
                                    'description': cata['description'],
                                    'max_days': cata['max_days'],
                                    'min_days': cata['min_days'],
                                    'category_id':cata['category_id'],
                                    'price': cata['price'],
                                    'status': cata['status'],
                                    'region': cata['region'],
                                    'county': cata['county'],
                                    'province': cata['province'],
                                    'category_name':ca.name,
                                    'category_description':ca.description,
                                    'ward_or_town': cata['ward_or_town'],
                                    'created_at': cata['created_at'],
                                    'updated_at': cata['updated_at']
                                }

                                dat.append(va)
                            data={
                                'data':dat,
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
def search_for_posts_2(request):
    """
    Search for posts based on location and category..Note: category_id,pages and items can't be null but other fields can be null
    -----
        {
            category_id:1,
            location_region: Changamwe
            location_county: Mombasa
            location_ward_or_town: Port Reltz
            page: 1
            items: 10
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':

            #Location_region and category_id are provided, other fields empty or none

            if request.data['location_region'] is not None and request.data['location_region'] != '':
                if request.data['category_id'] is not None and request.data['category_id'] != '':
                    if request.data['location_county'] is None or request.data['location_county'] == '':
                        if request.data['location_ward_or_town'] is None or request.data['location_ward_or_town'] == '':

                            location_region = request.data['location_region'] 
                            category_id=request.data['category_id']

                            loca = location.objects.filter(region=location_region)

                            page = request.GET.get('page', request.data['page'])
                            paginator = Paginator(loca, request.data['items'])
                            details=[]
                            deta = []
                            dat=[]
                            for loci in paginator.page(page):
                                values={
                                    'id':loci.id,
                                    'ward_or_town': loci.ward,
                                    'region': loci.region,
                                    'county': loci.county,
                                    'province': loci.province,
                                    'created_at': loci.created_at,
                                    'updated_at': loci.updated_at
                                }

                                details.append(values)

                            for cats in details:
                                cat = category.objects.get(category_id=category_id)
                                poster=posts.objects.filter(location_id = cats['id'])
                                for post in poster:
                                    val={
                                        'id':post.id,
                                        'user_id': post.user_id,
                                        'name': post.name,
                                        'description': post.description,
                                        'max_days': post.max_days,
                                        'min_days': post.min_days,
                                        'category_id':post.category_id,
                                        'price': post.price,
                                        'status': post.status,
                                        'region': cats['region'],
                                        'county': cats['county'],
                                        'province': cats['province'],
                                        'ward_or_town': cats['ward_or_town'],
                                        'category_name':cat.name,
                                        'category_description':cat.description,
                                        'created_at': post.created_at,
                                        'updated_at': post.updated_at
                                    }

                                    deta.append(val)
                            data={
                                'data':deta,
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
def search_for_posts_3(request):
    """
    Search for posts based on location and category..Note: category_id,pages and items can't be null but other fields can be null
    -----
        {
            category_id:1,
            location_region: Changamwe
            location_county: Mombasa
            location_ward_or_town: Port Reltz
            page: 1
            items: 10
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':

            if request.data['location_region'] is not None and request.data['location_region'] != '':
                if request.data['category_id'] is not None and request.data['category_id'] != '':
                    if request.data['location_county'] is not None and request.data['location_county'] != '':
                        if request.data['location_ward_or_town'] is None or request.data['location_ward_or_town'] == '':

                            location_region = request.data['location_region'] 
                            location_county = request.data['location_county']
                            category_id=request.data['category_id']

                            loca = location.objects.filter(region=location_region).filter(county = location_county)

                            page = request.GET.get('page', request.data['page'])
                            paginator = Paginator(loca, request.data['items'])
                            details=[]
                            deta = []
                            dat=[]
                            for loci in paginator.page(page):
                                values={
                                    'id':loci.id,
                                    'ward_or_town': loci.ward,
                                    'region': loci.region,
                                    'county': loci.county,
                                    'province': loci.province,
                                    'created_at': loci.created_at,
                                    'updated_at': loci.updated_at
                                }

                                details.append(values)

                            for cats in details:
                                cat = category.objects.get(category_id=category_id)
                                poster=posts.objects.filter(location_id = cats['id'])
                                for post in poster:
                                    val={
                                        'id':post.id,
                                        'user_id': post.user_id,
                                        'name': post.name,
                                        'description': post.description,
                                        'max_days': post.max_days,
                                        'min_days': post.min_days,
                                        'category_id':post.category_id,
                                        'price': post.price,
                                        'status': post.status,
                                        'region': cats['region'],
                                        'county': cats['county'],
                                        'province': cats['province'],
                                        'ward_or_town': cats['ward_or_town'],
                                        'category_name':cat.name,
                                        'category_description':cat.description,
                                        'created_at': post.created_at,
                                        'updated_at': post.updated_at
                                    }

                                    deta.append(val)
                            data={
                                'data':deta,
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
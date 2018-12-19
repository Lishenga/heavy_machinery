import os
from PIL import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pytz
import datetime
import random
import string
from machinery.models import adverts, adverts_logs, pricing_adverts, location, users, category


@api_view(['POST'])
def create_advert(request):
    """
    Create advert
    -----
        {
            user_id:1,
            location_id:1
            category_id:1
            name:cranes
            description: ruwerui
            pictures: roshies.jpg
            price_id:1
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST'and request.FILES['pictures']:
            for f in request.FILES.getlist('pictures'):
                size=30 
                chars=string.ascii_uppercase + string.digits
                newName_thumb = ''.join(random.choice(chars) for _ in range(size))+'_thumb'+'.png'
                basewidth = 300
                img = Image.open(f)
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((basewidth,hsize), Image.ANTIALIAS)
                img.save(os.path.join(settings.BASE_DIR, newName_thumb), format="png", quality=70)
                now = datetime.datetime.now()
                ad = adverts(
                    user_id=request.data['user_id'],
                    location_id=request.data['location_id'],  
                    category_id=request.data['category_id'], 
                    name=request.data['name'],
                    description=request.data['description'],
                    pictures=newName_thumb,
                    price_id=request.data['price_id'],
                    created_at = datetime.datetime.now(tz=pytz.UTC),
                    updated_at= datetime.datetime.now(tz=pytz.UTC)
                )
                ad.save()
                price = pricing_adverts.objects.get(id=request.data['price_id'])
                adder = adverts.objects.filter(name=request.data['name']).filter(description= request.data['description'])
                next = datetime.datetime.now(tz=pytz.UTC) + datetime.timedelta(minutes = int(price.time))
                for ads in adder:
                    logs = adverts_logs(
                        advert_id = ads.id,
                        nexttime = next,
                        created_at = datetime.datetime.now(tz=pytz.UTC),
                        updated_at= datetime.datetime.now(tz=pytz.UTC)
                    )
                    logs.save()
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
           }
        }
        return Response(error)        



#update existing location   
@api_view(['POST'])
def update_advert(request):    
    """
    Update advert details
    -----
        {
            id:1,
            user_id:1,
            location_id:1
            category_id:1
            name:cranes
            description: ruwerui
            pictures: roshies.jpg
            price_id:1
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST' and request.FILES['pictures']:
            fs = FileSystemStorage()
            ads = adverts.objects.filter(user_id=request.data['user_id'])
            for ad in ads:
                for f in request.FILES.getlist('pictures'):
                    if fs.exists(ad.pictures.path):
                        fs.delete(ad.pictures)

                        size=30 
                        chars=string.ascii_uppercase + string.digits
                        newName_thumb = ''.join(random.choice(chars) for _ in range(size))+'_thumb'+'.png'
                        basewidth = 300
                        img = Image.open(f)
                        wpercent = (basewidth/float(img.size[0]))
                        hsize = int((float(img.size[1])*float(wpercent)))
                        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
                        img.save(os.path.join(settings.BASE_DIR, newName_thumb), format="png", quality=70)

                        ad.user_id=request.data['user_id'],
                        ad.location_id=request.data['location_id'],  
                        ad.category_id=request.data['category_id'], 
                        ad.name=request.data['name'],
                        ad.description=request.data['description'],
                        ad.pictures=newName_thumb,
                        ad.price_id=request.data['price_id'],
                        ad.updated_at= datetime.date.today()
                        ad.save()

                    price = pricing_adverts.objects.get(id=request.data['price_id'])
                    adder = adverts.objects.filter(name=request.data['name']).filter(description= request.data['description'])
                    next = datetime.datetime.today() + datetime.timedelta(minutes = int(price.time))
                    for adds in adder:
                        adds.advert_id= ads.id
                        adds.nexttime = next
                        adds.updated_at= datetime.date.today()
                        
                        adds.save()
            success={'message':'success','status_code':200}
            return Response(success)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)            


#get all existing adverts
@api_view(['POST'])  
def get_all_adverts(request):  
    """
    See all adverts
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
            ad= adverts.objects.all()
            page = request.GET.get('page', request.data['page'])
            paginator = Paginator(ad, request.data['items'])
            details=[]
            deta=[]
            for ads in paginator.page(page):
                values={
                    'id':ads.id,
                    'user_id':ads.user_id,
                    'location_id':ads.location_id,
                    'category_id':ads.category_id,
                    'name':ads.name,
                    'description': ads.description,
                    'pictures': ads.pictures,
                    'price_id':ads.price_id,
                    'created_at': ads.created_at,
                    'updated_at': ads.updated_at
                }

                details.append(values)

            for cats in details:
                loc = location.objects.get(id=cats['location_id'])
                cate = category.objects.get(category_id=cats['category_id'])
                user = users.objects.get(id=cats['user_id'])
                ad_price = pricing_adverts.objects.get(id=cats['price_id'])
                val={
                    'id':cats['id'],
                    'user_id':cats['user_id'],
                    'category_name':cate.name,
                    'name': cats['name'],
                    'ad_owner': user.fname+' '+user.lname,
                    'description': cats['description'],
                    'location_county': loc.county,
                    'location_ward': loc.ward,
                    'pictures': cats['pictures'],
                    'ad_price': ad_price.price,
                    'ad_time': ad_price.time,
                    'ad_days': ad_price.days,
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


#get all existing adverts
@api_view(['POST'])  
def get_particular_user_adverts(request):  
    """
    Get particular user adverts(all)
    -----
        {
            user_id:1
            page:1
            items:10
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            ad= adverts.objects.filter(user_id=request.data['user_id'])
            page = request.GET.get('page', request.data['page'])
            paginator = Paginator(ad, request.data['items'])
            details=[]
            deta=[]
            for ads in paginator.page(page):
                values={
                    'id':ads.id,
                    'user_id':ads.user_id,
                    'location_id':ads.location_id,
                    'category_id':ads.category_id,
                    'name':ads.name,
                    'description': ads.description,
                    'pictures': ads.pictures,
                    'price_id':ads.price_id,
                    'created_at': ads.created_at,
                    'updated_at': ads.updated_at
                }

                details.append(values)

            for cats in details:
                loc = location.objects.get(id=cats['location_id'])
                cate = category.objects.get(category_id=cats['category_id'])
                user = users.objects.get(id=cats['user_id'])
                ad_price = pricing_adverts.objects.get(id=cats['price_id'])
                val={
                    'id':cats['id'],
                    'user_id':cats['user_id'],
                    'category_name':cate.name,
                    'name': cats['name'],
                    'ad_owner': user.fname+' '+user.lname,
                    'description': cats['description'],
                    'location_county': loc.county,
                    'location_ward': loc.ward,
                    'pictures': cats['pictures'],
                    'ad_price': ad_price.price,
                    'ad_time': ad_price.time,
                    'ad_days': ad_price.days,
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



#get one particelar advert details
@api_view(['POST'])  
def get_particular_advert_details(request):

    """
    Get particular advert details
    -----
        {
            id:1,
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':

            ad_id=request.data['id']
            ads=adverts.objects.get(id=ad_id)
            details=[]
            deta=[]
            values={
                'id':ads.id,
                'user_id':ads.user_id,
                'location_id':ads.location_id,
                'category_id':ads.category_id,
                'name':ads.name,
                'description': ads.description,
                'pictures': ads.pictures,
                'price_id':ads.price_id,
                'created_at': ads.created_at,
                'updated_at': ads.updated_at
            }

            details.append(values)

            for cats in details:
                loc = location.objects.get(id=cats['location_id'])
                cate = category.objects.get(category_id=cats['category_id'])
                user = users.objects.get(id=cats['user_id'])
                ad_price = pricing_adverts.objects.get(id=cats['price_id'])
                val={
                    'id':cats['id'],
                    'user_id':cats['user_id'],
                    'category_name':cate.name,
                    'name': cats['name'],
                    'ad_owner': user.fname+' '+user.lname,
                    'description': cats['description'],
                    'location_county': loc.county,
                    'location_ward': loc.ward,
                    'pictures': cats['pictures'],
                    'ad_price': ad_price.price,
                    'ad_time': ad_price.time,
                    'ad_days': ad_price.days,
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


@api_view(['DELETE'])
def delete_advert(request):
    """
    remove advert
    -----
        {
            id:1,
        }
    
    """
    try:
        if request.method=='DELETE':
            _id=request.data['id']
            fs = FileSystemStorage()
            delete=adverts.objects.filter(id=_id)
            for ad in delete:
                if fs.exists(os.path.join(settings.BASE_DIR, ad.pictures)):
                    fs.delete(os.path.join(settings.BASE_DIR, ad.pictures))

            delete.delete()     
            data={
                "data":delete,
                "message":"Advert deleted",
                "status_code":200
            }
            return Response(data)
        else:
            snippets={
                
                'message':"invalid request",
                "status_code":401
            }
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)
    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error) 



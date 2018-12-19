from machinery.help import helpers
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.paginator import Paginator
from PIL import Image
import os
import string
import random
import datetime
from machinery.models import user_items, gallery_items, location, category

@api_view(['POST'])
def create_item(request):
    """
    Create Item
    -----
        {
            user_id: 1 
            category_id: 1
            name: excavator,
            description: excavate things,
            price_for_lease: KSH 100 ,
            min_radius: 10,
            max_radius: 10,
            pictures: roshie.jpg
            location_id: 1,

        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST' and request.FILES['picture']:
            size=30 
            chars=string.ascii_uppercase + string.digits
            prevName = request.FILES['picture']
            newName = ''.join(random.choice(chars) for _ in range(size))+'.jpg'
            newName_thumb = ''.join(random.choice(chars) for _ in range(size))+'_thumb'+'.png'
            basewidth = 300
            img = Image.open(prevName)
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            fs = FileSystemStorage()
            filename = fs.save(newName, prevName)
            img.save(os.path.join(settings.BASE_DIR, newName_thumb), format="png", quality=70)
            #img_thumb = img.save(newName_thumb, format="png", quality=70)
            item = user_items(
                user_id=request.data['user_id'],
                category_id=request.data['category'],  
                name=request.data['name'],  
                description=request.data['description'], 
                price_for_lease=request.data['price_for_lease'], 
                location_id=request.data['location_id'],
                min_radius=request.data['min_radius'],
                max_radius=request.data['max_radius'],
                pictures=newName, 
                pictures_thumb= newName_thumb,
                created_at = datetime.date.today(),
                updated_at= datetime.date.today()
            )
            item.save()
            success={
                'message':'success',
                'status_code':200
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
def upload_multiple_pics_item(request):
    """
    Upload Pictures (Multiple)
    -----
        {
            user_item_id: 1 
            user_id: 1
            pictures: {}

        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST' and request.FILES['pictures']:
            for f in request.FILES.getlist('pictures'):
                size=30 
                chars=string.ascii_uppercase + string.digits
                prevName = request.FILES['pictures']
                newName = ''.join(random.choice(chars) for _ in range(size))+'.jpg'
                newName_thumb = ''.join(random.choice(chars) for _ in range(size))+'_thumb'+'.png'
                basewidth = 300
                img = Image.open(prevName)
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((basewidth,hsize), Image.ANTIALIAS)
                fs = FileSystemStorage()
                filename = fs.save(newName, prevName)
                img_thumb = img.save(newName_thumb, format="png", quality=70)
                item = gallery_items(
                    user_id=request.data['user_id'],
                    user_item_id=request.data['user_item_id'],  
                    pictures=newName, 
                    pictures_thumb= newName_thumb,
                    created_at = datetime.date.today(),
                    updated_at= datetime.date.today()
                )
                item.save()
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
                'category_id':request.data['category_id'],
                'name':request.data['name'],
                'description': request.data['description'],
                'price_for_lease': request.data['price_for_lease'],
           }
        }
        return Response(error)    


#update existing user    
@api_view(['POST'])
def update_item(request):    
    """
    Update item details
    -----
        {
            id:1,
            user_id: 1 
            category_id: 1
            name: excavator,
            description: excavate things,
            price_for_lease: KSH 100 ,
            min_radius: 10,
            max_radius: 10,
            location_id: 2,
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            fs = FileSystemStorage()
            item = user_items.objects.get(id=request.data['id'])
            if fs.exists(item.pictures.path) and fs.exists(item.pictures_thumb.path):
                fs.delete(item.pictures)
                fs.delete(item.pictures_thumb)

                size=30 
                chars=string.ascii_uppercase + string.digits
                prevName = request.FILES['pictures']
                newName = ''.join(random.choice(chars) for _ in range(size))+'.jpg'
                newName_thumb = ''.join(random.choice(chars) for _ in range(size))+'_thumb'+'.png'
                basewidth = 300
                img = Image.open(prevName)
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((basewidth,hsize), Image.ANTIALIAS)
                filename = fs.save(newName, prevName)
                img_thumb = img.save(newName_thumb, format="png", quality=70)

                item.name = request.data['name']
                item.description = request.data['description']
                item.user_id = request.data['user_id']
                item.category_id = request.data['category_id']
                item.price_for_lease = request.data['price_for_lease']
                item.location_id = request.data['location_id']
                item.pictures = newName
                item.pictures_thumb = newName_thumb
                item.updated_at = datetime.date.today()
                item.save()
                success={
                    'message':'success',
                    'status_code':200,
                    'location': request.data['location']
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
def get_all_items(request):  
    """
    Get all items
    -----
        {
            page: 1,
            items: 5
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            item= user_items.objects.all()
            page = request.GET.get('page', request.data['page'])
            paginator = Paginator(item, request.data['items'])
            fs = FileSystemStorage()
            details=[]
            deta=[]
            for items in paginator.page(page):
                values={
                    'id':items.id,
                    'user_id':items.user_id,
                    'category_id':items.category_id,
                    'name': items.name,
                    'description': items.description,
                    'location_id': items.location_id,
                    'pictures': items.pictures,
                    'pictures_thumb': items.pictures_thumb,
                    'price_for_lease': items.price_for_lease,
                    'max_radius': items.max_radius,
                    'min_radius':items.min_radius,
                    'status': items.status,
                    'created_at': items.created_at,
                    'updated_at': items.updated_at
                }

                details.append(values)

            for cats in details:
                loc = location.objects.get(id=cats['location_id'])
                cate = category.objects.get(category_id=cats['category_id'])
                val={
                    'id':cats['id'],
                    'user_id':cats['user_id'],
                    'category_name':cate.name,
                    'name': cats['name'],
                    'description': cats['description'],
                    'location_county': loc.county,
                    'location_ward': loc.ward,
                    'pictures': cats['pictures'],
                    'pictures_thumb': cats['pictures_thumb'],
                    'price_for_lease': cats['price_for_lease'],
                    'max_radius': cats['max_radius'],
                    'min_radius':cats['min_radius'],
                    'status': cats['status'],
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


#get all existing users
@api_view(['POST'])  
def get_all_gallery_items(request):  
    """
    Get all pictures for items
    -----
        {
            page: 1,
            items: 5
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            item= gallery_items.objects.all()
            page = request.GET.get('page', request.data['page'])
            paginator = Paginator(item, request.data['items'])
            details=[]
            for items in paginator.page(page):
                values={
                    'id':items.id,
                    'user_id':items.user_id,
                    'user_item_id':items.user_item_id,
                    'pictures': items.pictures,
                    'pictures_thumb': items.pictures_thumb,
                    'created_at': items.created_at,
                    'updated_at': items.updated_at
                }

                details.append(values)

                #paginator = Paginator(details, 10)

            data={'data':details,'message':'success','status_code':200}

            return Response(data)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)

#get one particular item details
@api_view(['POST'])  
def get_particular_item(request):

    """
    Get Particular item details
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
            item=user_items.objects.get(id=request.data['id'])
            details=[]
            deta=[]
            values={
                'id':item.id,
                'user_id':item.user_id,
                'category_id':item.category_id,
                'name': item.name,
                'description': item.description,
                'location_id': item.location_id,
                'price_for_lease': item.price_for_lease,
                'pictures': item.pictures,
                'pictures_thumb': item.pictures_thumb,
                'max_radius': item.max_radius,
                'min_radius':item.min_radius,
                'status': item.status,
                'created_at': item.created_at,
                'updated_at': item.updated_at
            }

            details.append(values)

            for cats in details:
                loc = location.objects.get(id=cats['location_id'])
                cate = category.objects.get(category_id=cats['category_id'])
                val={
                    'id':cats['id'],
                    'user_id':cats['user_id'],
                    'category_name':cate.name,
                    'name': cats['name'],
                    'description': cats['description'],
                    'location_county': loc.county,
                    'location_ward': loc.ward,
                    'pictures': cats['pictures'],
                    'pictures_thumb': cats['pictures_thumb'],
                    'price_for_lease': cats['price_for_lease'],
                    'max_radius': cats['max_radius'],
                    'min_radius':cats['min_radius'],
                    'status': cats['status'],
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

#get one particular item details
@api_view(['POST'])  
def get_gallery_pics_for_item(request):

    """
    Get all gallery pics for a particular item
    -----
        {
            item_id:1,
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':
            item=gallery_items.objects.filter(id=request.data['item_id'])
            details=[]
            deta=[]
            for items in item:
                values={
                    'id':items.id,
                    'user_id':items.user_id,
                    'user_item_id':items.user_item_id,
                    'pictures': items.pictures,
                    'pictures_thumb': items.pictures_thumb,
                    'created_at': items.created_at,
                    'updated_at': items.updated_at
                }

                details.append(values)

                #paginator = Paginator(details, 10)

            data={'data':details,'message':'success','status_code':200}

            return Response(data)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)


#get particular user item details
@api_view(['POST'])  
def get_particular_user_items(request):

    """
    Get particular user item details
    -----
        {
            user_id:1,
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':
            item=user_items.objects.filter(user_id=request.data['user_id'])
            page = request.GET.get('page', request.data['page'])
            paginator = Paginator(item, request.data['items'])
            details=[]
            deta=[]
            for items in paginator.page(page):
                values={
                    'id':items.id,
                    'user_id':items.user_id,
                    'category_id':items.category_id,
                    'name': items.name,
                    'description': items.description,
                    'location_id': items.location_id,
                    'price_for_lease': items.price_for_lease,
                    'pictures': items.pictures,
                    'pictures_thumb': items.pictures_thumb,
                    'max_radius': items.max_radius,
                    'min_radius':items.min_radius,
                    'status': items.status,
                    'created_at': items.created_at,
                    'updated_at': items.updated_at
                }

                details.append(values)

            for cats in details:
                loc = location.objects.get(id=cats['location_id'])
                cate = category.objects.get(category_id=cats['category_id'])
                val={
                    'id':cats['id'],
                    'user_id':cats['user_id'],
                    'category_name':cate.name,
                    'name': cats['name'],
                    'description': cats['description'],
                    'location_county': loc.county,
                    'location_ward': loc.ward,
                    'pictures': cats['pictures'],
                    'pictures_thumb': cats['pictures_thumb'],
                    'price_for_lease': cats['price_for_lease'],
                    'max_radius': cats['max_radius'],
                    'min_radius':cats['min_radius'],
                    'status': cats['status'],
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

def delete_item(request):
    """
    remove item
    -----
        {
            id:1,
        }
    
    """
    try:
        if request.method=='DELETE':
            _id=request.data['id']

            delete=user_items.objects.filter(id=_id).delete()
            data={
                "data":delete,
                "message":"Item deleted",
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
            "message":'Item not deleted',
            "status_code":500
        }
        return Response(data)   



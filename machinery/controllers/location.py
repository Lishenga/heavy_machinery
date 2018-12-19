from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from machinery.models import location
from django.core.paginator import Paginator
import datetime



@api_view(['POST'])
def create_location(request):
    """
    Create Location
    -----
        {
           
            region:juja,
            county:kiambu,
            province:central,
            ward_or_town: juja
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            locations = location(
                region=request.data['region'],
                county=request.data['county'],  
                province=request.data['province'], 
                ward=request.data['ward_or_town'],
                created_at = datetime.date.today(),
                updated_at= datetime.date.today()
            )
            locations.save()
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
                'region':request.data['region'],
                'county':request.data['county'],
                'province':request.data['province']
           }
        }
        return Response(error)        



#update existing location   
@api_view(['POST'])
def update_location(request):    
    """
    Update location details
    -----
        {
            id:1,
            region:juja,
            county:kiambu,
            province:central,
            ward_or_town: juja
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            locations = location.objects.get(id=request.data['id'])
            locations.region = request.data['region']
            locations.county=request.data['county']
            locations.province=request.data['province'],
            locations.ward=request.data['ward_or_town'],
            locations.save()
            success={'message':'success','status_code':200}
            return Response(success)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)            


#get all existing locations
@api_view(['POST'])  
def get_all_locations(request):  
    """
    See all Locations
    -----
        {
            page:1
            items: 5
        }
    """
    try:
        locationss= location.objects.all()
        page = request.GET.get('page', request.data['page'])
        paginator = Paginator(locationss, request.data['items'])
        details=[]
        for loci in paginator.page(page):
            values={
                'id':loci.id,
                'region': loci.region,
                'county': loci.county,
                'province': loci.province,
                'ward_or_town': loci.ward,
                'created_at': loci.created_at,
                'updated_at': loci.updated_at
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



#get one particelar location details
@api_view(['POST'])  
def get_particular_location_details(request):

    """
    Get particular location details
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

            location_id=request.data['id']
            loci=location.objects.get(id=location_id)
            details={
                'id':loci.id,
                'ward_or_town': loci.ward,
                'region': loci.region,
                'county': loci.county,
                'province': loci.province,
                'created_at': loci.created_at,
                'updated_at': loci.updated_at
            }

            data={'data':details,'message':'success','status_code':200}

            return Response(data)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)


@api_view(['DELETE'])
def delete_location(request):
    """
    remove location
    -----
        {
            id:1,
        }
    
    """
    try:
        if request.method=='DELETE':
            _id=request.data['id']

            delete=location.objects.filter(id=_id).delete()
            data={
                "data":delete,
                "message":"Location deleted",
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



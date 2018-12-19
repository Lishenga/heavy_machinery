from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from machinery.models import pricing_adverts,adverts,location,adverts_logs
from django.core.paginator import Paginator
import datetime
import pytz


@api_view(['POST'])
def create_pricing_adverts(request):
    """
    Create pricing adverts
    -----
        {
           
            name:premium,
            description:jkdfjklfjkdfjk,
            days:4,
            price: 500
            time: 5
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            adsprice = pricing_adverts(
                name=request.data['name'],
                description=request.data['description'],  
                days=request.data['days'], 
                price=request.data['price'],
                time=request.data['time'],
                created_at = datetime.datetime.today(),
                updated_at= datetime.datetime.today()
            )
            adsprice.save()
            success={
                'message':'success',
                'status_code':200
            }
            return Response(success)
            
    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
        }
        return Response(error)        



#update existing location   
@api_view(['POST'])
def update_advert_price(request):    
    """
    Update adverts pricing details
    -----
        {
            id:1,
            name:premium,
            description:jkdfjklfjkdfjk,
            days:4,
            price: 500
            time: 5
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            adspricing = pricing_adverts.objects.get(id=request.data['id'])
            adspricing.name=request.data['name'],
            adspricing.description=request.data['description'],  
            adspricing.days=request.data['days'], 
            adspricing.price=request.data['price'],
            adspricing.time=request.data['time'],
            adspricing.updated_at= datetime.date.today()
            adspricing.save()
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
def get_all_adspricing(request):  
    """
    See all adspricing
    -----
        {
            page:1
            items: 5
        }
    """
    try:
        adspricing = pricing_adverts.objects.all()
        page = request.GET.get('page', request.data['page'])
        paginator = Paginator(adspricing, request.data['items'])
        details=[]
        for ad in paginator.page(page):
            values={
                'id':ad.id,
                'name': ad.name,
                'description': ad.description,
                'price': ad.price,
                'days': ad.days,
                'time':ad.time,
                'created_at': ad.created_at,
                'updated_at': ad.updated_at
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



#get one particelar adspricing details
@api_view(['POST'])  
def get_particular_adspricing_details(request):

    """
    Get particular advert pricing details
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

            id=request.data['id']
            ad = pricing_adverts.objects.get(id=id)
            details=[]
            values={
                'id':ad.id,
                'name': ad.name,
                'description': ad.description,
                'pricing': ad.pricing,
                'days': ad.days,
                'time':ad.time,
                'created_at': ad.created_at,
                'updated_at': ad.updated_at
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


@api_view(['DELETE'])
def delete_adspricing(request):
    """
    remove adspricing
    -----
        {
            id:1,
        }
    
    """
    try:
        if request.method=='DELETE':
            _id=request.data['id']

            delete=pricing_adverts.objects.filter(id=_id).delete()
            data={
                "data":delete,
                "message":"adspricing deleted",
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



#get all existing adverts basing on pricing
@api_view(['POST'])  
def get_all_adverts_basing_pricing(request):  
    """
    See all adverts basing on pricing(Premium, standard etc)
    -----
        {
            page:1
            items: 5
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':
            ad = adverts.objects.all()
            page = request.GET.get('page', request.data['page'])
            details=[]
            detai=[]
            deta=[]
            for ads in ad:
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

            for ca in details:
                loci = location.objects.get(id=ca['location_id'])
                v={
                    'id':ca['id'],
                    'user_id':ca['user_id'],
                    'ward_or_town': loci.ward,
                    'region': loci.region,
                    'county': loci.county,
                    'province': loci.province,
                    'category_id':ca['category_id'],
                    'name':ca['name'],
                    'description':ca['description'],
                    'pictures':ca['pictures'],
                    'price_id':ca['price_id'],
                    'created_at':ca['created_at'],
                    'updated_at':ca['updated_at']
                }

                detai.append(v)

            paginator = Paginator(detai, request.data['items'])

            for cats in paginator.page(page):
                adpricing = pricing_adverts.objects.get(id = cats['price_id'])
                logs= adverts_logs.objects.filter(advert_id=cats['id']).latest('nexttime')
                time = datetime.datetime.now(tz=pytz.UTC) - cats['updated_at']
                if time.days < int(adpricing.days) and datetime.datetime.now(tz=pytz.UTC) > logs.nexttime:
                    val={
                        'id':cats['id'],
                        'user_id':cats['user_id'],
                        'ward_or_town': cats['ward_or_town'],
                        'region': cats['region'],
                        'county': cats['county'],
                        'province': cats['province'],
                        'category_id':cats['category_id'],
                        'name':cats['name'],
                        'description':cats['description'],
                        'pictures':cats['pictures'],
                        'price_id':cats['price_id'],
                        'created_at':cats['created_at'],
                        'updated_at':cats['updated_at']
                    }

                    deta.append(val)
                    next = datetime.datetime.now(tz=pytz.UTC) + datetime.timedelta(minutes = int(adpricing.time))
                    log = adverts_logs(
                        advert_id = cats['id'],
                        nexttime = next,
                        created_at = datetime.datetime.now(tz=pytz.UTC),
                        updated_at= datetime.datetime.now(tz=pytz.UTC)
                    )

                    log.save()

            data={
                'data':deta,
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


#get all existing adverts basing on pricing
@api_view(['POST'])  
def get_all_adverts_basing_location(request):  
    """
    See all adverts basing on location
    -----
        {
            page:1
            items: 5
            location_county: Lamu
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':
            ad = adverts.objects.all()
            page = request.GET.get('page', request.data['page'])
            details=[]
            detai=[]
            deta=[]
            for ads in ad:
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

            for ca in details:
                loci = location.objects.filter(county=request.data['location_county']).get(id=ca['location_id'])
                v={
                    'id':ca['id'],
                    'user_id':ca['user_id'],
                    'ward_or_town': loci.ward,
                    'region': loci.region,
                    'county': loci.county,
                    'province': loci.province,
                    'category_id':ca['category_id'],
                    'name':ca['name'],
                    'description':ca['description'],
                    'pictures':ca['pictures'],
                    'price_id':ca['price_id'],
                    'created_at':ca['created_at'],
                    'updated_at':ca['updated_at']
                }

                detai.append(v)

            paginator = Paginator(detai, request.data['items'])

            for cats in paginator.page(page):
                adpricing = pricing_adverts.objects.get(id = cats['price_id'])
                logs= adverts_logs.objects.filter(advert_id=cats['id']).latest('nexttime')
                time = datetime.datetime.now(tz=pytz.UTC) - cats['updated_at']
                if time.days < int(adpricing.days) and datetime.datetime.now(tz=pytz.UTC) > logs.nexttime:
                    val={
                        'id':cats['id'],
                        'user_id':cats['user_id'],
                        'ward_or_town': cats['ward_or_town'],
                        'region': cats['region'],
                        'county': cats['county'],
                        'province': cats['province'],
                        'category_id':cats['category_id'],
                        'name':cats['name'],
                        'description':cats['description'],
                        'pictures':cats['pictures'],
                        'price_id':cats['price_id'],
                        'created_at':cats['created_at'],
                        'updated_at':cats['updated_at']
                    }

                    deta.append(val)
                    next = datetime.datetime.now(tz=pytz.UTC) + datetime.timedelta(minutes = int(adpricing.time))
                    log = adverts_logs(
                        advert_id = cats['id'],
                        nexttime = next,
                        created_at = datetime.datetime.now(tz=pytz.UTC),
                        updated_at= datetime.datetime.now(tz=pytz.UTC)
                    )

                    log.save()

            data={
                'data':deta,
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
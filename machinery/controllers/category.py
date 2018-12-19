from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from machinery.models import category
from machinery.help import helpers
import datetime



@api_view(['POST'])
def create_category(request):
    """
    Create category
    -----
        {
           
            name: pickups,
            description:what the category entails,
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            categories = category(
                name=request.data['name'],
                description=request.data['description'],  
                created_at = datetime.date.today(),
                updated_at= datetime.date.today()
            )
            categories.save()
            log=helpers.create_log(request= request, tags="category", description="category Created")
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
                'name':request.data['name'],
                'description':request.data['description']
           }
        }
        return Response(error)        



#update existing category    
@api_view(['POST'])
def update_category(request):    
    """
    Update category details
    -----
        {
            id:1,
            name: pickups,
            description:what the category entails,
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            categories = category.objects.get(category_id=request.data['id'])
            categories.name = request.data['name']
            categories.description=request.data['description']
            categories.save()
            success={'message':'success','status_code':200}
            return Response(success)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)            


#get all existing categories
@api_view(['GET'])  
def get_all_categories(request): 
    
    try: 
        categories= category.objects.all()
        details=[]
        for cat in categories:
            values={
                'id':cat.category_id,
                'name': cat.name,
                'description': cat.description,
                'status': cat.status,
                'created_at': cat.created_at,
                'updated_at': cat.updated_at
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



#get one particular category's details
@api_view(['POST'])  
def get_particular_category_details(request):

    """
    Update user details
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

            categories=category.objects.get(category_id=request.data['id'])
            details={
                'id':categories.id,
                'name': categories.name,
                'description': categories.description,
                'status': categories.status,
                'created_at': categories.created_at,
                'updated_at': categories.updated_at
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

def delete_category(request):
    """
    remove category
    -----
        {
            id:1,
        }
    
    """
    try:
        if request.method=='DELETE':
            _id=request.data['id']

            delete=category.objects.filter(category_id=_id).delete()
            data={
                "data":delete,
                "message":"Category deleted",
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



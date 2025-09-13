from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
# Create your views here.

# implementing deserializer in product list as it should take data from user via post and update in db
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
    # select_related makes site load faster as it loads the related field and makes less time to render so when we render product their collection also gets loaded
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many = True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data = request.data)
        # validationg data
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
             

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
        product = get_object_or_404(Product, pk=id)
        # retriving the data
        if request.method == 'GET':
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        # to update the product
        elif request.method == 'PUT':
            serializer = ProductSerializer(product, data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            # here orderitems is related name in model OrderItem 
            if product.orderitems.count() > 0:
                  return Response({'error': 'Product cannot be deleted because it is associated with order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)        


@api_view()
def collection_detail(request, pk):
      return Response('ok')
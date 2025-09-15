from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
# Create your views here.


# IMPLEMENTING GENERIC VIEWS
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    





# # THIS IS CLASS BASED VIEWS

# class ProductList(APIView):
#     def get(self, request):
#     # select_related makes site load faster as it loads the related field and makes less time to render so when we render product their collection also gets loaded
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many = True, context={'request': request})
#         return Response(serializer.data)
     
#     def post(self, request):
#         serializer = ProductSerializer(data = request.data)
#         # validationg data
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)



class ProductDetail(APIView):
     
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
     
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
     


# ThHIS CODE IS FUNCTION BASED IT IS CHANGED INTO CLASS BASED

# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#     # select_related makes site load faster as it loads the related field and makes less time to render so when we render product their collection also gets loaded
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many = True, context={'request': request})
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = ProductSerializer(data = request.data)
#         # validationg data
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
        
             

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, id):
#         product = get_object_or_404(Product, pk=id)
#         # retriving the data
#         if request.method == 'GET':
#             serializer = ProductSerializer(product)
#             return Response(serializer.data)
#         # to update the product
#         elif request.method == 'PUT':
#             serializer = ProductSerializer(product, data = request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)
#         elif request.method == 'DELETE':
#             # here orderitems is related name in model OrderItem 
#             if product.orderitems.count() > 0:
#                   return Response({'error': 'Product cannot be deleted because it is associated with order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#             product.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)        


# GENERIC VIEW OF COLLECTION LIST
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializer
    def get_serializer_context(self):
        return {'request', self.request}
    



    
# # API VIEW OF COLLECTION LIST
# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#     # select_related makes site load faster as it loads the related field and makes less time to render so when we render collection and their product count also gets loaded
#     # here in Count() if we write related_name in foreign key in product we must write it otherwise we can write product
#         queryset = Collection.objects.annotate(products_count = Count('products')).all()
#         serializer = CollectionSerializer(queryset, many = True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data = request.data)
#         # validationg data
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
        










@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, id):
        collection = get_object_or_404(Collection.objects.annotate(
             products_count=Count('products')
        ), pk=id)
        # retriving the data
        if request.method == 'GET':
            serializer = CollectionSerializer(collection)
            return Response(serializer.data)
        # to update the product
        elif request.method == 'PUT':
            serializer = CollectionSerializer(collection, data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            if collection.products.count() > 0:
                 return Response({'error': 'Collection cannot be deleted as it includes one or more'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            collection.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  
from ast import Raise, Try
from webbrowser import get
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from . models import Product, OrderItem, Review
from . serialiszer import ProductSerializer, ReviewSerializer
from rest_framework import status
from store import serialiszer


#Product serializer using from rest_framework.generics import ListCreateAPIView,
# class ProductList(ListCreateAPIView):
#     def get_queryset(self):
#         return Product.objects.select_related('collection').all()

#     def get_serializer_class(self):
#         return ProductSerializer

#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serialiszer = ProductSerializer(queryset, many=True)
#         return Response(serialiszer.data)

#     def get_serializer_context(self):
#         return super().get_serializer_context()

#Product serializer using from rest_framework.generics import RetrieveUpdateDestroyAPIView,
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def delete(self, request,pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({"error" : "Cannot delete this product because it is related to an order item"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# APIView.
# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serialiszer = ProductSerializer(queryset, many=True)
#         return Response(serialiszer.data)

#     def post(self, request):
#         serialiszer = ProductSerializer(data=request.data)
#         serialiszer.is_valid(raise_exception=True)
#         serialiszer.save()
#         return Response(serialiszer.data, status=status.HTTP_201_CREATED)

# class ProductDetail(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serialiszer = ProductSerializer(product)
#         return Response(serialiszer.data)

#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serialiszer = ProductSerializer(product, data=request.data)
#         serialiszer.is_valid(raise_exception=True)
#         serialiszer.save()

#     def detele(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# function based
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()
#         serialiszer = ProductSerializer(queryset, many=True)
#         return Response(serialiszer.data)
#     elif request.method == 'POST':
#         serialiszer = ProductSerializer(data=request.data)
#         serialiszer.is_valid(raise_exception=True)
#         serialiszer.save()
#         return Response(serialiszer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def get_product_detail(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         serialiszer = ProductSerializer(product)
#     elif request.method == 'PUT':
#         serialiszer = ProductSerializer(product, data=request.data)
#         serialiszer.is_valid(raise_exception=True)
#         serialiszer.save()
#     elif request.method == 'DELETE':
#        # if product.order_item
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     return Response(serialiszer.data)

#Product serializer using from rest_framework.viewsets import ModelViewSet
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_serializer_class(self):
        return ProductSerializer
    
    def get_serializer_context(self):
        return {'request' : self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response({"error" : "Cannot delete this product because it is related to an order item"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
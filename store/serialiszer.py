from decimal import Decimal
from pyexpat import model
from turtle import title
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from store.models import Product, Review

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)

#class ProductSerializer(serializers.Serializer):
class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    #collection = CollectionSerializer()
    class Meta:
        model = Product
        #fields = '__all__'
        fields = ['id', 'title', 'price', 'price_with_tax', 'inventory', 'collection']
        
    def calculate_tax(self, product):
        return product.unit_price *  Decimal(1.1)
    
    # def create(self, validated_data):
    #     collection = CollectionSerializer()
    #     collection.is_valid(raise_exception=True)
    #     collection.save()
    #     return Product.objects.create(**validated_data)
    
class ReviewSerializer(serializers.ModelSerializer):
    model = Review
    fields = ['id', 'name', 'description', 'date', 'product']
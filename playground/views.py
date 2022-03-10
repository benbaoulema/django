# pylint: disable=unused-import
import imp
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Value, F, Func
from django.db.models.aggregates import Max, Min, Avg, Count, Sum
from django.contrib.contenttypes.models import ContentType

from store.models import Product, OrderItem
from tags.models import TaggedItem;

from store.models import Product, OrderItem

# Create your views here.

def say_hello(request):
    try:
        #products = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
        #products = Product.objects.filter(inventory= F('unit_price'))
        #products = Product.objects.order_by('title')
        #products = Product.objects.order_by('unit_price', '-title')
        #products = Product.objects.values('title', 'unit_price', 'collection__title')
       # queryset = OrderItem.objects.values('product_id').distinct()
        products = Product.objects.select_related('collection').all()
        product_count = Product.objects.aggregate(Count('id'))
        full_name = Func(F('first_name'), F('last_name'), function='CONCAT')
        queryset = TaggedItem.objects.get_tags_for(Product, 1)
    except ObjectDoesNotExist:
        pass
    return render(request, 'hello.html', {'name': "Sylla", 'products': list(products), 'product_count': product_count, 'tags' : list(queryset)})

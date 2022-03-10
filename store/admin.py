from django.contrib import admin
from django.db.models.aggregates import Max, Min, Avg, Count, Sum
from django.utils.html import format_html, urlencode
from django.urls import reverse

from . import models
# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]
    def queryset(self, request, queryset):
        if self.value() == '<10' :
            return queryset.filter(inventory__lt = 10)
    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_per_page = 30
    list_filter = ['collection', 'last_update', InventoryFilter]

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10 :
            return 'Low'
        return 'Ok'
    
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} product(s) were successfully updated. ' 
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'membership', 'phone']
    list_editable = ['phone', 'membership']
    search_fields = ['last_name']
    list_filter = ['membership']
    list_per_page = 30

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer' ,'payment_status', 'placed_at']

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title' ,'products_count']
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id' : collection.id})
        return format_html('<a href="{}">{}<a/>', url, collection.products_count)
        
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

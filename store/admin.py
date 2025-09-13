from django.db.models import Count
from django.contrib import admin
from . import models
from django.utils.html import format_html, urlencode
from django.urls import reverse
# Register your models here.


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>10', 'High')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        if self.value() == '>10':
            return queryset.filter(inventory__gt = 10)
        

        





@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'products_count']
    # to implement search in dropdown in add product
    search_fields = ['title']

    
    @admin.display(ordering='products_count')
    def products_count(self, Collection):
        url = (reverse('admin:store_product_changelist')
                + '?'
                + urlencode({
                    'collection__id': str(Collection.id)
                }))
        return format_html('<a href="{}">{}</a>', url, Collection.products_count)
        
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
            
            )
    










@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields =['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields= ['title']

    def collection_title(self, product):
        return product.collection.title
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory <25:
            return 'Low'
        return 'OK'







@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership','orders_count']
    # to implement search in dropdown in add order
    search_fields = ['first_name','last_name']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']


    @admin.display(ordering='orders_count')
    def orders_count(self, Customer):
        url = (reverse('admin:store_order_changelist')
                + '?'
                + urlencode({
                    'customer__id': str(Customer.id)
                }))
        return format_html('<a href="{}">{} Orders</a>', url, Customer.orders_count)
        
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
            
            )
    



class OrderItemInLine(admin.StackedInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    min_num =1
    max_num = 10
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInLine]
    list_per_page = 10
    list_select_related = ['customer']

    def custoer_title(self, order):
        name = order.customer.fname+' '+order.customer.lname
        return name
    
    






@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['description', 'discount']
    list_per_page = 10
    ordering = ['description']









    
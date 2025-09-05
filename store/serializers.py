from rest_framework import serializers
from decimal import Decimal

from store.models import Product, Collection


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)

    # here unit_price is changed to price and passed argument source = unit_price ie. actual name in product class
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price' )
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    collection = serializers.PrimaryKeyRelatedField(
        queryset = Collection.objects.all()
        # this will return a field collection with its id
    ) 
    #  this method we can add new field in api ie. price_with tax
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    


    # to implement serializing relations we import Collection model
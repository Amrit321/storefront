from rest_framework import serializers
from decimal import Decimal

from store.models import Product, Collection, Review





# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length = 255 )



# creation model serializer
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only = True)



# creation model serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']
        # so after using model serializer we do not need to do as below
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)

    # # here unit_price is changed to price and passed argument source = unit_price ie. actual name in product class
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price' )
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = serializers.HyperlinkedRelatedField(
    #    queryset = Collection.objects.all(),
    #    view_name = 'collection-detail'
    # )
    


    
    # collection = CollectionSerializer()
    # this CollectionSerializer() includes the nested objects ie each collection is rendered as object


    # collection = serializers.StringRelatedField() 
    # convert each collection to string object and return it here
    # this will return a field collection with its id 
    
    
    #  this method we can add new field in api ie. price_with tax
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    


    # to implement serializing relations we import Collection model


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'date', 'description']
        
    # this function to create the id of the product extract in views.py so it will automatically insert the id of the specific product
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id = product_id, **validated_data)

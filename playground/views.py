from django.shortcuts import render
from store.models import Customer
from django.db.models import Value, F, Func
from store.models import OrderItem

from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem
# Create your views here.
# request -> response
# request handeler
# action
def say_hello(request):
      content_type = ContentType.objects.get_for_model(Product)
      
      queryset = Product.objects.filter()[:5]
      
      
    

   
      return render(request, 'hello.html', {'name': 'Amrit Chapagain', 'products':list(queryset)})

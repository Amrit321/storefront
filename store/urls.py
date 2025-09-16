from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
router.urls

urlpatterns = router.urls

# urlpatterns = [

    
    
#     # this below for generic views
#     # path('products/', views.ProductList.as_view()),
#     # path('products/<int:pk>/', views.ProductDetail.as_view()),
#     # path('collections/', views.CollectionList.as_view()),
#     # path('collections/<int:pk>/', views.CollectionDetail.as_view()),
    
#     # path('collections/<int:pk>/', views.collection_detail, name='collection-detail')
#     # path('products/', views.product_list),
#     # path('products/<int:id>/', views.product_detail),
    
#  ] 


        
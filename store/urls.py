from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view()),
     path('collections/<int:id>/', views.ProductDetail.as_view()),
    # path('products/', views.product_list),
    path('collections/', views.collection_list),
    # path('products/<int:id>/', views.product_detail),
    path('collections/<int:id>/', views.collection_detail, name='collection-detail')
]
        
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('products', views.products, name='products'),
    path('products/my-products', views.my_products, name='My Products'),
    path('products/add-update-product', views.add_update_product,
         name='Add/Update Product'),
    path('products/add-product', views.add_product,
         name='Add Product'),
    path('products/delete-product', views.delete_product,
         name='Delete Product'),
    path('products/top-products', views.top_products, name='Top Products'),
]

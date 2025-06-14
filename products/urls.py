from django.urls import path
from . import views
from .views import buy_product

urlpatterns = [
    path('', views.product_list, name='products'),  # تغيير الاسم إلى 'products'
    path('home', views.home, name='home'),
    path('product-details/<int:product_id>/', views.product_detail, name='product_detail'),
    path('buy/<int:product_id>/', buy_product, name='buy_product'),
    
]

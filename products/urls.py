from django.urls import path
from . import views
from .views import buy_product

urlpatterns = [
    path('', views.product_list, name='products'),
    path('home', views.home, name='home'),
    path('product-details/<int:product_id>/', views.product_detail, name='product_detail'),
    path('buy/<int:product_id>/', buy_product, name='buy_product'),
    
    # Cart URLs
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('update-cart/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Order URLs
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Review URLs
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
    
    # Notification URLs
    path('notifications/', views.notifications, name='notifications'),
    path('mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('delete-notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('mark-all-notifications-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('clear-all-notifications/', views.clear_all_notifications, name='clear_all_notifications'),
    path('check-new-notifications/', views.check_new_notifications, name='check_new_notifications'),
]

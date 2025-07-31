from django.contrib import admin
from .models import (
    Product, Purchase, Advertisement, Cart, Order, OrderItem, 
    Review, Coupon, Notification
)

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'active', 'created_at']
    list_filter = ['category', 'active']
    search_fields = ['name', 'content']
    list_editable = ['active', 'price']

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['buyer_name', 'product_name', 'price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['buyer_name', 'product_name']

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at', 'expires_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username']
    list_editable = ['status']
    
    def save_model(self, request, obj, form, change):
        """Override save to ensure notifications are sent when status changes"""
        if change:  # This is an update
            old_obj = Order.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                # Status changed, notification will be sent by the model's save method
                pass
        super().save_model(request, obj, form, change)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order__status']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'product__name']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percentage', 'is_active', 'valid_from', 'valid_to', 'used_count']
    list_filter = ['is_active', 'valid_from', 'valid_to']
    search_fields = ['code']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title']

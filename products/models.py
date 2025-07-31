from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
 

# Create your models here.
class Product(models.Model):
    category=[
        ('electronics', 'Electronics'),
        ('laptop', 'laptop'),
        ('desktop', 'desktop'),
        ('all in one computer','all_in_one_computer'),
        ('mobile', 'mobile'),
        ('tablet', 'tablet'),
        ('accessories', 'accessories'),
        ('gaming', 'gaming'),
        ('printer', 'printer'),
        ('camera', 'camera'),
        ('audio', 'audio'),
        ('networking', 'networking'),
        ('software', 'software'),
        ('home appliances', 'home_appliances'),
        ('smart home devices', 'smart_home_devices')
        # Add more categories as needed

    ]
    name = models.CharField(max_length=100,verbose_name='Product Name')
    content = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField( upload_to='photos/%y/%m/%d')
    active = models.BooleanField(default=True)
    category = models.CharField(max_length=100, verbose_name='Category',choices=category,default=category[0][0])
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Check if this is an update and active status changed from False to True
        if self.pk:  # This is an update
            old_instance = Product.objects.get(pk=self.pk)
            if not old_instance.active and self.active:
                # Product is now active (restocked), notify users who might be interested
                from django.db.models import Q
                interested_users = Userstore.objects.filter(
                    Q(cart__product=self) | Q(notification__notification_type='product_restock')
                ).distinct()
                
                for user in interested_users:
                    Notification.objects.create(
                        user=user,
                        title=f'{self.name} is back in stock!',
                        message=f'Good news! {self.name} is now available again.',
                        notification_type='product_restock',
                    )
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'items'
        verbose_name_plural = 'shop'
        ordering = ['name'] 
# This model represents a product in the e-commerce application.



class Advertisement(models.Model):
    title = models.CharField(max_length=200)  # عنوان الإعلان
    description = models.TextField(blank=True, null=True)  # وصف الإعلان
    image = models.ImageField(upload_to='ads/')  # صورة الإعلان
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ الإنشاء
    expires_at = models.DateTimeField(blank=True, null=True)  # تاريخ انتهاء الإعلان
    is_active = models.BooleanField(default=True)  # حالة الإعلان (مفعل أو غير مفعل)
    products = models.ManyToManyField(Product, related_name='advertisements', blank=True)  # علاقة المنتجات المرتبطة بالإعلان

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # If this is a new advertisement, notify all users
        if not self.pk and self.is_active:
            from store.models import Userstore
            users = Userstore.objects.all()
            
            for user in users:
                Notification.objects.create(
                    user=user,
                    title=f'New Promotion: {self.title}',
                    message=f'{self.description or "Check out our latest promotion!"}',
                    notification_type='promotion',
                )
        
        super().save(*args, **kwargs)

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buyer_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.buyer_name} - {self.product_name}"


# Cart System
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} x{self.quantity}"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity


# Order System
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        # Check if this is an update and status has changed
        if self.pk:  # This is an update
            old_instance = Order.objects.get(pk=self.pk)
            old_status = old_instance.status
            new_status = self.status
            
            # If status changed, create notification
            if old_status != new_status:
                status_messages = {
                    'processing': 'Your order is now being processed',
                    'shipped': 'Your order has been shipped and is on its way',
                    'delivered': 'Your order has been delivered successfully',
                    'cancelled': 'Your order has been cancelled'
                }
                
                if new_status in status_messages:
                    Notification.objects.create(
                        user=self.user,
                        title=f'Order #{self.order_number} Status Updated',
                        message=f'{status_messages[new_status]}. Order #{self.order_number}',
                        notification_type='order_status',
                    )
        else:
            # This is a new order
            if not self.order_number:
                self.order_number = str(uuid.uuid4())[:8].upper()
        
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
    
    def __str__(self):
        return f"{self.order.order_number} - {self.product.name} x{self.quantity}"
    
    @property
    def total_price(self):
        return self.price * self.quantity


# Review System
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}/5)"


# Coupon System
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    max_usage = models.PositiveIntegerField(default=100)
    used_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
    
    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"
    
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return (self.is_active and 
                self.valid_from <= now <= self.valid_to and 
                self.used_count < self.max_usage)


# Notification System
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('order_status', 'Order Status'),
        ('product_restock', 'Product Restock'),
        ('promotion', 'Promotion'),
        ('system', 'System'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='system')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


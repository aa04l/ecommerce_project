from django.db import models
from django.conf import settings
 

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
    ##year_model=models.DateField(default='2025', verbose_name='Year Model')
    ##time=models.TimeField(null=True)
    ##created_at = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.name
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

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buyer_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.buyer_name} - {self.product_name}"


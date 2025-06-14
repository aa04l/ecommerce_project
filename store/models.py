from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
class Store(models.Model):
    name = models.CharField(max_length=100, verbose_name='Store Name')
    location = models.CharField(max_length=255, verbose_name='Location')
    contact_number = models.CharField(max_length=15, verbose_name='Contact Number', null=True, blank=True)
    email = models.EmailField(verbose_name='Email Address', null=True, blank=True)
    opening_hours = models.CharField(max_length=100, verbose_name='Opening Hours', null=True, blank=True)
    about= models.TextField(verbose_name='About Store', null=True, blank=True)
    image = models.ImageField(upload_to='store_photos/%y/%m/%d', verbose_name='Store Image', null=True, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'
        ordering = ['name']
# Create your models here.


class Userstore(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    
    def __str__(self):
        return self.username
    


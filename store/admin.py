from django.contrib import admin
from .models import Userstore
# Register your models here.
from .models import Store
admin.site.register(Store)
admin.site.register(Userstore)
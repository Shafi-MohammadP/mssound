from django.contrib import admin
from .models import Order, OrderItem,Itemstatus,Orderstatus
# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Itemstatus)
admin.site.register(Orderstatus)

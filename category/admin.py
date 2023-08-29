from django.contrib import admin
from .models  import category


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}



admin.site.register(category)

from django.contrib import admin
from .models import Product, ProductReview


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview)

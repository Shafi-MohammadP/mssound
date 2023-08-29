from django.urls import path
from .import views

urlpatterns = [
    path('shop_filter', views.Shop_Filtering, name='Shop_Filter')
]

from . import views
from django.urls import path

urlpatterns = [
    path('coupon', views.coupon, name='coupon'),
    path('add_coupon', views.add_coupon, name='addcoupon'),
    path('edit_coupon/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
    path('delete_coupon/<int:coupon_id>/',
         views.delete_coupon, name='delete_coupon'),
]

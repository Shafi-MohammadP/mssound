from django.urls import path
from . import views

urlpatterns=[
    
    path('cart',views.cart,name='cart'),
    path('remove_cart<int:cart_id>',views.remove_cart,name='remove_cart'),
    path('add_cart',views.add_cart,name='add_cart'),
    path('update_cart/',views.update_cart,name='update_cart'),
      
]
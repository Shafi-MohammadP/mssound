from django.urls import path
from . import views

urlpatterns = [
    path('wishlist', views.wishlist, name="wishlist"),
    path('add_wishlist', views.add_wishlist, name='add_wishlist'),
    path('wish_remove<int:remove_id>', views.wish_remove, name="wish_remove"),
    # path('wishproduct_show/<int:prod_id>/<int:img_id>',
    #      views.wish_product_show, name='wishproduct_show'),
    path('add_wish_list', views.add_wish_list, name='add_wish_list')
]

from django.urls import path, include
from .import views
urlpatterns = [
    path('', views.home, name='home'),
    path('product_show/<int:prod_id>/<int:img_id>',
         views.product_show, name='product_show'),
    path('shop', views.shop, name='shop'),
    path('search_view', views.search_view, name='search_view'),
    path('QuickView/<int:product_id>/<int:image_id>',
         views.QuickView, name='quickview'),
    path('product_list', views.product_list, name='product_list'),
    path('track_order', views.track_order, name='track_order'),
    path('Contact_Us', views.Contact_Us, name='ContactUs'),
    path('Contact_User', views.Contact_User, name='contact_user')



]

from django.urls import path
from . import views

urlpatterns = [
    path('order_list/', views.order_list, name="order_list"),
    path('viewOrder/<int:view_id>/', views.viewOrder, name="viewOrder"),
    path('change_status', views.change_status, name="change_status"),
    path('cancel_order/<int:cancel_id>',
         views.cancel_order, name='cancel_order'),
    path('return_order/<int:return_id>', views.return_order, name='return_order')
]

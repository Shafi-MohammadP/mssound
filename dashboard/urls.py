from django.urls import path
from . import views

urlpatterns = [

    path('', views.admin_login1, name='admin_login1'),
    path('admin_signup', views.admin_signup, name='admin_signup'),
    path('usermanagement_1', views.usermanagement_1, name='usermanagement_1'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('admin_forgotpassword', views.admin_forgotpassword,
         name='admin_forgotpassword'),
    path('adminlogout', views.admin_logout1, name='admin_logout1'),
    path('userlisitng', views.users_listing, name='users_listing'),
    path('dashboardog', views.dashboardog, name='dashboardog'),
    path('blockuser/<int:user_id>', views.blockuser, name='blockuser'),
    path('salesrepost', views.sales_report, name='sales_report'),
    path('dowload_CSC', views.Dowload_CSV, name='export_csv'),
    path('dowload_PDF', views.generate_pdf, name='Dowload_PDF'),
    path('searchuser', views.search_user, name='Searching_user'),
    path('user_status_search', views.user_status_search, name='user_status_search'),

]

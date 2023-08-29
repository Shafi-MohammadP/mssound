from django.urls import path, include
from .import views
urlpatterns = [

    path('user_login', views.user_login1, name='user_login1'),
    path('user-signup', views.user_signup, name='user_signup'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('logout1/', views.logout1, name='logout1'),


]

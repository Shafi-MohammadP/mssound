from django.urls import path
from . import views

urlpatterns=[
  path('', views.categories, name='categories'),
  path('add_category/', views.add_category, name='add_category'),
  path('search_category/', views.search_category, name='search_category'),
  path('editcategory/<slug:editcategory_id>', views.editcategory, name='editcategory'),
  path('deletecategory/<slug:deletecategory_id>', views.deletecategory, name='deletecategory'),
]
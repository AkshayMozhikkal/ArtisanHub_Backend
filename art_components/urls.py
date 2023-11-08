
from django.urls import path, include
from .views import *

urlpatterns = [
    
    path('banners/', Banner_List_Create.as_view(), name='banners'),
    path('banner_edit/<int:id>/', Banner_Edit_Delete.as_view(), name='banner_edit'),
   
]
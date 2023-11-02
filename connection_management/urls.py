
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Connections.as_view(), name='connections'),
    path('connection_request/', Connection_Request.as_view(), name='connection_request'),
    path('connection_handle/<int:pk>/', AcceptRejectConnection.as_view(), name='connection_handle'),
    path('connection_status/<int:to_user_id>/', Connection_Status.as_view(), name='connection_status'),
    path('remove_connection/<int:id>/', Delete_Connection.as_view(), name='remove_connection'),
    path('user_connections/<int:user_id>', UserConnectionsView.as_view(), name='user_connections'),
    path('search_connection/<int:user_id>/<str:search_key>', Search_Connection.as_view(), name='search_connection'),
]
 
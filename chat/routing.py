from django.urls import path
from .consumers import ChatConsumer
from decouple import config

soc=config('socket')
websocket_urlpatterns = [
    path(f'{soc}<int:id>/', ChatConsumer.as_asgi()),
]
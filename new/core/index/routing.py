from django.urls import path
from . import consumers

app_name = 'ws'

websocket_urlpatterns = [
    path('ws/project/<int:project_id>/', consumers.ChatConsumer.as_asgi(), name='room'),
]

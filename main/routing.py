from django.urls import re_path
from .consumer import Chat
websocket_urlpatterns = [
# re_path(r'ws/main/(?P<room_name>\w+)/$',Chat.as_asgi()),
re_path(r'ws/main/',Chat.as_asgi()),

]


from django.urls import re_path

from . import group_consumers, friends_consumers

websocket_urlpatterns = [
    re_path(r'ws/group/chat/(?P<room_name>\w+)/$', group_consumers.GroupChatConsumer.as_asgi()),
    re_path(r'ws/friend/chat/(?P<room_name>\w+)/$', friends_consumers.FriendsChatConsumer.as_asgi()),
]
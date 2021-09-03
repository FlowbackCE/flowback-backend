# FlowBack was created and project lead by Loke Hagberg. The design was
# made by Lina Forsberg. Emilio Müller helped constructing Flowback.
# Astroneatech created the code. It was primarily financed by David
# Madsen. It is a decision making platform.
# Copyright (C) 2021  Astroneatech AB
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/.

from django.urls import re_path

from . import group_consumers, friends_consumers

websocket_urlpatterns = [
    re_path(r'ws/group/chat/(?P<room_name>\w+)/$', group_consumers.GroupChatConsumer.as_asgi()),
    re_path(r'ws/friend/chat/(?P<room_name>\w+)/$', friends_consumers.FriendsChatConsumer.as_asgi()),
]
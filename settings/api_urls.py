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

from rest_framework.routers import DefaultRouter
from django.urls import path
from django.conf.urls import url, include

from django_rest_passwordreset import views as reset_pass_view

from flowback.base.api.routers import SingletonRouter
from flowback.users.views import UserViewSet, UserLogin, CurrentUserViewSet, UserGroupViewSet, UserLogout, \
    LocationViewSet, FriendsViewSet, GroupChatViewSet
from flowback.polls.views import GroupPollViewSet
from flowback.notifications.urls import urlpatterns as notification_urls

default_router = DefaultRouter(trailing_slash=False)
singleton_router = SingletonRouter(trailing_slash=False)
default_router.register("user", UserViewSet, basename="user")
default_router.register("me", CurrentUserViewSet, basename="me")
default_router.register("user_group", UserGroupViewSet, basename="user_group")
default_router.register("group_poll", GroupPollViewSet, basename="group_poll")
default_router.register("location", LocationViewSet, basename="location")
default_router.register("friend", FriendsViewSet, basename="friend")
default_router.register('group_chat', GroupChatViewSet, basename='group_chat')

urlpatterns = default_router.urls + singleton_router.urls + notification_urls + [
    path("login", UserLogin.as_view(), name="user-login"),
    path("logout", UserLogout.as_view(), name="user-logout"),
    url(r'^password_reset/validate_token/',
        reset_pass_view.ResetPasswordValidateToken.as_view(authentication_classes=[], permission_classes=[]),
        name="reset-password-validate"),
    url(r'^password_reset/confirm/',
        reset_pass_view.ResetPasswordConfirm.as_view(authentication_classes=[], permission_classes=[]),
        name="reset-password-confirm"),
    url(r'^password_reset/',
        reset_pass_view.ResetPasswordRequestToken.as_view(authentication_classes=[], permission_classes=[]),
        name='reset-password-request')
]

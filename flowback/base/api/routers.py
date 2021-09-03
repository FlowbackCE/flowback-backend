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

# Third Party Modules
from rest_framework import routers


class SingletonRouter(routers.SimpleRouter):
    """Same as default router but without detail route and GET, POST, PUT, PATCH and
    DELETE maps to same url as list.

    See CurrentUserViewset for usages. This allows GenericViewSet to be used against
    a singleton resource. If `/me` endpoint represents currently logged in user
    you are able to `GET /me`, `PUT /me`, `DELETE /me` and can also add any list_routes like
    `POST /me/change-avatar`.
    """
    routes = [
        # Mapping for list, create, update, partial_update and delete function to http verb.
        routers.Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create',
                'patch': 'partial_update',
                'put': 'update',
                'delete': 'destroy',
            },
            name='{basename}',
            detail=False,
            initkwargs={'suffix': ''}
        ),
        # Dynamically generated list routes.
        # Generated using @action decorator
        # on methods of the viewset.
        routers.DynamicRoute(
            url=r'^{prefix}/{url_path}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
    ]

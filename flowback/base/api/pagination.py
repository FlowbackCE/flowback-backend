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
from rest_framework.pagination import PageNumberPagination as DrfPageNumberPagination


class PageNumberPagination(DrfPageNumberPagination):

    # Client can control the page using this query parameter.
    page_query_param = 'page'

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = 'per_page'

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = 1000


def paginated_response(request, queryset, serializer_class, extra_context=None):
    '''Utlity function to return a paginated response.

    Returns `Response` object with pagination info after serializing the django
    `queryset` as per the `serializer_class` given and processing the current
    `page` from the `request` object.

    If `extra_context`(dict) is provided, it will be passed to the serializer_class
    as context variables.
    '''
    paginator = PageNumberPagination()
    paginated_queryset = paginator.paginate_queryset(queryset=queryset, request=request)
    serializer_context = {'request': request}

    if extra_context:
        serializer_context.update(extra_context)

    serializer = serializer_class(paginated_queryset, context=serializer_context, many=True)
    return paginator.get_paginated_response(data=serializer.data)

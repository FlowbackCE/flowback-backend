import datetime

from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from flowback.notifications.mixins import ApiErrorsMixin
from flowback.notifications.pagination import get_paginated_response, LimitOffsetPagination

from flowback.notifications.selectors import user_notification_list, user_notification_subscriptions
from flowback.notifications.services import user_notification_read, user_notification_subscribe, \
    user_notification_unsubscribe, NotificationTypeValidator
from flowback.notifications.models import UserNotifications, NotificationSubscribers


class NotificationListApi(ApiErrorsMixin, APIView):
    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):  # Pycharm bug
        id = serializers.IntegerField(required=False)

        type = serializers.CharField(required=False)
        target = serializers.IntegerField(required=False)
        link_type = serializers.CharField(required=False)
        link_target = serializers.IntegerField(required=False)

        is_read = serializers.NullBooleanField(required=False)
        date = serializers.DateTimeField(required=False)

    def validate_date(self, obj):
        if obj > datetime.datetime.now():
            raise ValidationError('Datetime filter exceeds current time.')

    class OutputSerializer(serializers.ModelSerializer):
        link = serializers.SerializerMethodField()

        class Meta:
            model = UserNotifications
            fields = (
                'type',
                'target',
                'link_type',
                'link_target',
                'message',
                'read',
                'date'
            )

        def get_link(self, obj):
            return NotificationTypeValidator(notification_type=obj.type, notification_target=obj.target).link

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        notifications = user_notification_list(user=request.user, filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=notifications,
            request=request,
            view=self
        )


class NotificationSubscriptionsApi(ApiErrorsMixin, APIView):
    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class OutputSerializer(serializers.ModelSerializer):
        link = serializers.SerializerMethodField()

        class Meta:
            model = NotificationSubscribers
            fields = (
                'type',
                'target'
            )

        def get_link(self, obj):
            return NotificationTypeValidator(notification_type=obj.type, notification_target=obj.target).link

    def get(self, request):
        subscriptions = user_notification_subscriptions(user=request.user)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=subscriptions,
            request=request,
            view=self
        )


class NotificationSubscribedApi(ApiErrorsMixin, APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        notification_type = serializers.ChoiceField((
            'group', 'poll', 'proposal'
        ))
        notification_target = serializers.IntegerField()

    def get(self, request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        get_object_or_404(NotificationSubscribers,
                          type=serializer.notification_type,
                          target=serializer.notification_target)

        return Response(status=status.HTTP_302_FOUND)


class NotificationUpdateApi(ApiErrorsMixin, APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        read = serializers.BooleanField(default=True)

    def post(self, request, notification_id):
        serializer = self.InputSerializer(data=request.data)
        serializer = serializer.is_valid(raise_exception=True)

        user_notification_read(user=request.user,
                               notification=notification_id,
                               **serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class NotificationSubscribeApi(ApiErrorsMixin, APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        notification_type = serializers.ChoiceField((
            'group', 'poll', 'proposal'
        ))
        notification_target = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer = serializer.is_valid(raise_exception=True)

        user_notification_subscribe(notification_type=serializer.notification_type,
                                    notification_target=serializer.notification_target,
                                    user=request.user)

        return Response(status=status.HTTP_201_CREATED)


class NotificationUnsubscribeApi(ApiErrorsMixin, APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        notification_type = serializers.ChoiceField((
            'group', 'poll', 'proposal'
        ))
        notification_target = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer = serializer.is_valid(raise_exception=True)

        user_notification_unsubscribe(notification_type=serializer.notification_type,
                                      notification_target=serializer.notification_target,
                                      user=request.user)

        return Response(status=status.HTTP_200_OK)

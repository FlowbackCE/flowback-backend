# Selectors go here (database get queries)
# https://github.com/HackSoftware/Django-Styleguide#selectors
import django_filters

from flowback.users.models import User
from flowback.notifications.models import Notification, UserNotifications, NotificationSubscribers


class NotificationFilter(django_filters.FilterSet):
    class Meta:
        model = Notification
        fields = ('type', 'target', 'message', 'read', 'date')


class NotificationSubscribersFilter(django_filters.FilterSet):
    class Meta:
        model = NotificationSubscribers
        fields = 'user'


class UserNotificationSubscriptionsFilter(django_filters.FilterSet):
    class Meta:
        model = NotificationSubscribers
        fields = ('type', 'target')


# User notifications
def user_notification_list(*, user: User, filters=None):
    filters = filters or {}

    qs = UserNotifications.objects.filter(user=user).all()

    return NotificationFilter(filters, qs)


# User subscriptions list
def user_notification_subscriptions(*, user: User, filters=None):
    filters = filters or {}

    qs = NotificationSubscribers.objects.filter(user=user).all()

    return UserNotificationSubscriptionsFilter(filters, qs)


# Users in subscription list
def notification_subscriber_list(*, notification_type: str, notification_target: int, filters=None):
    filters = filters or {}

    qs = NotificationSubscribers.objects.filter(type=notification_type, target=notification_target).all()

    return NotificationSubscribersFilter(filters, qs)

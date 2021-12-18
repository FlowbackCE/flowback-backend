# Selectors go here (database get queries)
# https://github.com/HackSoftware/Django-Styleguide#selectors
import django_filters

from flowback.users.models import User
from flowback.notifications.models import UserNotifications, NotificationSubscribers


class UserNotificationFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name='notification__type', lookup_expr='iexact')
    target = django_filters.NumberFilter(field_name='notification__target', lookup_expr='iexact')

    class Meta:
        model = UserNotifications
        fields = ('id',
                  'notification__id',
                  'notification__type',
                  'notification__target',
                  'notification__link_type',
                  'notification__link_target',
                  'notification__message',
                  'notification__date',
                  'read')


class NotificationSubscribersFilter(django_filters.FilterSet):
    class Meta:
        model = NotificationSubscribers
        fields = ['user']


class UserNotificationSubscriptionsFilter(django_filters.FilterSet):

    class Meta:
        model = NotificationSubscribers
        fields = ['type', 'target']


# User notifications
def user_notification_list(*, user: User, filters=None):
    filters = filters or {}

    qs = UserNotifications.objects.filter(user=user).all()

    return UserNotificationFilter(filters, qs).qs


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

# Services goes here (database post queries & methods)
# https://github.com/HackSoftware/Django-Styleguide#services
import datetime

from flowback.users.models import User
from django.core.exceptions import ValidationError
from flowback.notifications.models import Notification, UserNotifications, NotificationSubscribers
from flowback.notifications.selectors import user_notification_subscriptions, user_notification_list, \
    notification_subscriber_list


# Notifies all subscribers related to the notification target
def notify_subscribers(notification: Notification):
    subscribers = notification_subscriber_list(
        notification_type=notification.type,
        notification_target=notification.target
    )
    UserNotifications.objects.bulk_create(
        [NotificationSubscribers(
            user=user,
            type=notification.type,
            target=notification.target
        ) for user in subscribers.data]
    )


# Creates a notification & notifies all users related to the topic
def notification_create(
        *,
        notification_type: object,
        notification_target: int,
        link_type: object,
        link_target: int,
        message: str,
        date: datetime.datetime
) -> Notification:
    notification = Notification(
        type=notification_type,
        target=notification_target,
        link_type=link_type,
        link_target=link_target,
        message=message,
        date=date
    )
    notification.full_clean()
    notification.save()
    notify_subscribers(notification)

    return notification


# Deletes a notification
def notification_delete(
        *,
        notification_type: str,
        notification_target: int,
        link_type: str,
        link_target: int
):
    Notification.objects.filter(
        type=notification_type,
        target=notification_target,
        link_type=link_type,
        link_target=link_target
    ).delete()

    NotificationSubscribers.objects.get(
        type=notification_type,
        target=notification_target
    ).delete()


# Mark notification as read/unread
def user_notification_read(*, notification: Notification, user: User, read: bool):
    user_notification = UserNotifications.objects.get(user=user, notification=notification)
    user_notification.read = read
    user_notification.save()


# Subscribe to a topic
# TODO add security to ensure that the target exist
def user_notification_subscribe(*, notification_type: str, notification_target: int, user: User):
    if user in notification_subscriber_list(
        notification_type=notification_type,
        notification_target=notification_target
    ):
        raise ValidationError(f'User {user} is already subscribed.')

    NotificationSubscribers.objects.create(
        user=user,
        type=notification_type,
        target=notification_target
    )


# Unsubscribe to a topic
def user_notification_unsubscribe(*, notification_type: str, notification_target: int, user: User):
    if user not in notification_subscriber_list(
        notification_type=notification_type,
        notification_target=notification_target
    ):
        raise ValidationError(f'User {user} is already unsubscribed.')

    NotificationSubscribers.objects.filter(
        user=user,
        type=notification_type,
        target=notification_target
    ).delete()

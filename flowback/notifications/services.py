# Services goes here (database post queries & methods)
# https://github.com/HackSoftware/Django-Styleguide#services
import datetime

from flowback.users.models import User, Group
from flowback.users.services import user_group_permitted
from flowback.polls.models import Poll, PollProposal
from django.core.exceptions import ValidationError
from flowback.notifications.models import Notification, UserNotifications, NotificationSubscribers
from flowback.notifications.selectors import notification_subscriber_list


# Get relevant data of a notification target
class NotificationTypeValidator:
    def __init__(self, *, notification_type: str, notification_target: int):
        if notification_type == 'group':
            self.type = Group
            self.target = Group.objects.get(id=notification_target)
            self.group = self.target
            self.link = f'groupdetails/{self.group.id}'

        if notification_type == 'poll':
            self.type = Poll
            self.target = Poll.objects.get(id=notification_target)
            self.group = self.target.group
            self.link = f'groupdetails/{self.group.id}/pollDetails/{notification_target}'

        if notification_type == 'proposal':
            self.type = PollProposal
            self.target = PollProposal.objects.get(id=notification_target)
            self.group = self.target.poll.group
            self.link = f'groupdetails/{self.group.id}/pollDetails/{notification_target}'

        else:
            raise ValidationError('Invalid Notification Type')


# Notifies all subscribers related to the notification target
def notify_subscribers(notification: Notification):
    subscribers = notification_subscriber_list(
        notification_type=notification.type,
        notification_target=notification.target
    )
    UserNotifications.objects.bulk_create(
        [UserNotifications(
            user=user,
            notification=notification,
            read=False
        ) for user in subscribers.data]
    )


# Creates a notification & notifies all users related to the topic
def notification_create(
        *,
        notification_type: str,
        notification_target: int,
        link_type: str,
        link_target: int,
        message: str,
        date: datetime.datetime
) -> Notification:
    NotificationTypeValidator(notification_type=notification_type, notification_target=notification_target)
    NotificationTypeValidator(notification_type=link_type, notification_target=link_target)
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


def notification_update(
        *,
        message: str = None,
        date: datetime.datetime = None,
        notification_type: str,
        notification_target: int,
        link_type: str,
        link_target: int
) -> None:
    data = {}
    if message:
        data['message'] = message
    if date:
        data['date'] = date
    NotificationTypeValidator(notification_type=notification_type, notification_target=notification_target)
    NotificationTypeValidator(notification_type=link_type, notification_target=link_target)
    Notification.objects.filter(type=notification_type,
                                target=notification_target,
                                link_type=link_type,
                                link_target=link_target).update(**data)


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
def user_notification_read(*, user: User, notification: int, read: bool):
    notification = UserNotifications.objects.get(notification=notification)

    if not notification.user == user:
        raise ValidationError('Notification does not belong to user')

    notification.read = read
    notification.save()


# Subscribe to a topic
def user_notification_subscribe(*, notification_type: str, notification_target: int, user: User):
    if user in notification_subscriber_list(
        notification_type=notification_type,
        notification_target=notification_target
    ):
        raise ValidationError(f'User is already subscribed.')

    validator = NotificationTypeValidator(notification_type=notification_type, notification_target=notification_target)
    user_group_permitted(user, group_id=validator.group.id)

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

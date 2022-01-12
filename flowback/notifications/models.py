from django.db import models
from flowback.base.models import TimeStampedModel
from flowback.users.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class NotificationBase(models.Model):
    class Type(models.TextChoices):
        GROUP = 'GROUP', _('group')
        POLL = 'POLL', _('poll')
        PROPOSAL = 'PROPOSAL', _('proposal')
        # POLL_PROPOSAL = 'POLL_PROPOSAL', _('poll_proposal')  # Subscribe to poll proposals comments
        # POLL_COMMENT = 'POLL_COMMENT_REPLY', _('poll_comment_reply')  # Subscribe to poll proposal comment reply

    type = models.CharField(choices=Type.choices, max_length=255)
    target = models.IntegerField()

    class Meta:
        abstract = True


# All notifications goes in Notification model
class Notification(TimeStampedModel, NotificationBase):
    link_type = models.CharField(choices=NotificationBase.Type.choices, max_length=255)  # The target link
    link_target = models.IntegerField()  # The link target id
    message = models.TextField()  # The notification itself
    date = models.DateTimeField()  # When to notify the subscribers

    @property
    def is_active(self) -> bool:
        now = timezone.now()

        return self.date <= now.date()


# NotificationUser is a many to many relationship between user and notification
class UserNotifications(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)


class NotificationSubscribers(TimeStampedModel, NotificationBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'type', 'target')

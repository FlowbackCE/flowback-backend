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
import datetime

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin, UserManager)
from rest_framework.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager

from flowback.base.models import TimeStampedUUIDModel

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email, last_login=now)
        user.set_password(password)
        user.username = email
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        return self.create_user(email, password)


# A user model which doesn't extend AbstractUser
class User(AbstractBaseUser, PermissionsMixin, TimeStampedUUIDModel):
    """
        An abstract base class implementing a fully featured User model with
        admin-compliant permissions.
        Username and password are required. Other fields are optional.
        """

    NORMAL_USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER_TYPES = (NORMAL_USER, ADMIN, MODERATOR)
    USER_TYPE_CHOICES = (
        (NORMAL_USER, _('User')),
        (ADMIN, _('Admin')),
        (MODERATOR, _('Moderator')),
    )

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    user_type = models.CharField(_('User Type'), max_length=45, db_index=True,
                                 choices=USER_TYPE_CHOICES, default=NORMAL_USER)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    image = models.ImageField(null=True, blank=True)
    cover_image = models.ImageField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    accepted_terms_use = models.BooleanField(default=False)
    accepted_terms_condition = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    phone_number = PhoneNumberField(_('phone number'), unique=True,
                                    null=True, blank=True, db_index=True,
                                    help_text='Include the country code.')
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_name(self):
        """Return full name if available, else username."""
        full_name = self.get_full_name()
        if full_name != '':
            return full_name
        else:
            return self.username


class Group(TimeStampedUUIDModel):
    DIRECT_JOIN = 'direct_join'
    NEEDS_MODERATION = 'need_moderation'
    MEMBER_REQUEST_TYPE_CHOICES = (
        (DIRECT_JOIN, _('Direct Join')),
        (NEEDS_MODERATION, _('Needs Moderation')),
    )
    DIRECT_APPROVE = 'direct_approve'
    POLL_APPROVAL_TYPE_CHOICES = (
        (DIRECT_APPROVE, _('Direct Approve')),
        (NEEDS_MODERATION, _('Needs Moderation')),
    )

    owners = models.ManyToManyField(User, related_name="group_owners")
    admins = models.ManyToManyField(User, related_name="group_admins")
    moderators = models.ManyToManyField(User, related_name="group_moderators")
    members = models.ManyToManyField(User, related_name="group_members")
    delegators = models.ManyToManyField(User, related_name='group_delegators')
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='group/image/')
    tag = TaggableManager()
    cover_image = models.ImageField(null=True, blank=True, upload_to='group/cover_img/')
    public = models.BooleanField(default=True)
    members_request = models.CharField(_('Member Request Type'), max_length=50, choices=MEMBER_REQUEST_TYPE_CHOICES,
                                       default=DIRECT_JOIN)
    poll_approval = models.CharField(_('Poll Request Type'), max_length=50, choices=POLL_APPROVAL_TYPE_CHOICES,
                                     default=DIRECT_APPROVE)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    room_name = models.CharField(max_length=100, default='default')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_groups")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="updated_by")
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)


class GroupRequest(TimeStampedUUIDModel):
    REQUESTED = 'requested'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    REQUEST_TYPE_CHOICES = (
        (REQUESTED, _('Requested')),
        (ACCEPTED, _('Accepted')),
        (REJECTED, _('Rejected')),
    )

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participant')
    status = models.CharField(max_length=100, choices=REQUEST_TYPE_CHOICES, default=REQUESTED)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_by')

    class Meta:
        unique_together = ('group', 'participant')


class GroupDocs(TimeStampedUUIDModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_name')
    doc = models.FileField(upload_to='group/docs/')
    doc_name = models.CharField(max_length=256)
    created_by = models.ForeignKey(User, related_name='grp_doc_created_by', on_delete=models.CASCADE)


class OnboardUser(TimeStampedUUIDModel):
    email = models.EmailField(unique=True)
    screen_name = models.CharField(max_length=50)
    verification_code = models.IntegerField()
    is_verified = models.BooleanField(default=False)


class PasswordReset(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verification_code = models.IntegerField(unique=True)

    def clean(self):
        if not self.created_at <= self.created_at + datetime.timedelta(hours=1):
            raise ValidationError('Verification code has expired')


class Country(models.Model):
    country_name = models.CharField(max_length=100)


class State(models.Model):
    state_name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class City(models.Model):
    city_name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)


class Friends(TimeStampedUUIDModel):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_sender')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_receiver')
    room_name = models.CharField(max_length=100)
    request_accept = models.BooleanField(default=False)
    request_accepted_at = models.DateTimeField(blank=True, null=True)
    request_sent_at = models.DateTimeField(auto_now_add=True, editable=False)
    block = models.BooleanField(default=False)


class FriendChatMessage(TimeStampedUUIDModel):
    TEXT_MESSAGE = 'text'
    MESSAGE_TYPE_CHOICES = (
        (TEXT_MESSAGE, _('Text')),
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver_sender")
    message = models.TextField()
    message_type = models.CharField(max_length=100, choices=MESSAGE_TYPE_CHOICES, default=TEXT_MESSAGE)
    seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField(blank=True, null=True)


class GroupChatMessage(TimeStampedUUIDModel):
    TEXT_MESSAGE = 'text'
    MESSAGE_TYPE_CHOICES = (
        (TEXT_MESSAGE, _('Text')),
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_message_sender")
    message = models.TextField()
    message_type = models.CharField(max_length=100, choices=MESSAGE_TYPE_CHOICES, default=TEXT_MESSAGE)
    seen_by = models.ManyToManyField(User)
from unittest.mock import patch
import datetime

from django.urls import reverse
from django.test import TestCase
from flowback.users.models import User
from django.core.exceptions import ValidationError
from rest_framework import status

from flowback.notifications.services import notification_create, notification_update, notification_delete
from flowback.notifications.models import Notification

from flowback.polls.models import Group, Poll, PollProposal
from flowback.polls.serializer import PollProposalCreateSerializer, PollProposalEventCreateSerializer


class NotificationTestBaseClass(TestCase):
    def setUp(self) -> None:
        # Create User
        def generate_user(mail, passwd):
            user = dict(
                email=mail,
                username=mail,
                password=passwd,
                accepted_terms_condition=True
            )
            return User.objects.create(**user)

        def generate_group(user, title):
            group = dict(
                created_by=user,
                updated_by=user,
                title=title,
                description='Example Description',
                public=True,
                members_request='direct_join',
                poll_approval='direct_approve',
                country='Sweden',
                city='Stockholm'
            )
            return Group.objects.create(**group)

        def generate_poll(user, group, title, poll_type):
            poll = dict(
                created_by=user,
                modified_by=user,
                group=group,
                title=title,
                description="Example Description",
                type=poll_type,
                start_time=datetime.datetime.now(),
                end_time=datetime.datetime.now() + datetime.timedelta(hours=1)
            )
            return Poll.objects.create(**poll)

        def generate_proposals(user, *polls):
            x = 0
            for poll in polls:
                data = dict(poll=poll.id, proposal=f'some_{user.id}_proposal_{x}')
                serializer = PollProposalCreateSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=user)
                x += 1

        def generate_event_proposals(user, *event_polls):
            x = 0
            for poll in event_polls:
                data = dict(poll=poll.id, proposal=f'some_{user.id}_proposal_{x}',
                            date=datetime.datetime.now() + datetime.timedelta(hours=1))
                serializer = PollProposalEventCreateSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=user)

        self.user_one = generate_user('a@a.se', 'pwd')
        self.user_two = generate_user('b@b.se', 'pwd')
        self.user_three = generate_user('c@c.se', 'pwd')
        self.user_four = generate_user('d@d.se', 'pwd')
        self.user_five = generate_user('e@e.se', 'pwd')

        self.group_one = generate_group(self.user_one, 'E1')
        self.group_two = generate_group(self.user_two, 'E2')

        self.poll_one = generate_poll(self.user_one, self.group_one, 'P1', Poll.Type.POLL)
        self.poll_two = generate_poll(self.user_two, self.group_one, 'P2', Poll.Type.POLL)
        self.poll_three = generate_poll(self.user_one, self.group_two, 'P3', Poll.Type.POLL)

        self.poll_mission_one = generate_poll(self.user_one, self.group_one, 'PM1', Poll.Type.MISSION)
        self.poll_mission_two = generate_poll(self.user_two, self.group_one, 'PM2', Poll.Type.MISSION)
        self.poll_mission_three = generate_poll(self.user_one, self.group_two, 'PM3', Poll.Type.MISSION)

        self.poll_event_one = generate_poll(self.user_one, self.group_one, 'PE1', Poll.Type.EVENT)
        self.poll_event_two = generate_poll(self.user_two, self.group_one, 'PE2', Poll.Type.EVENT)
        self.poll_event_three = generate_poll(self.user_one, self.group_two, 'PE3', Poll.Type.EVENT)

        generate_proposals(self.user_one, *[self.poll_one, self.poll_two])
        generate_proposals(self.user_two, *[self.poll_one, self.poll_two])
        generate_proposals(self.user_three, *[self.poll_one, self.poll_two])


class NotificationCreationTests(NotificationTestBaseClass):
    def test_creating_notification(self):
        notification = notification_create(
            notification_type=Poll,
            notification_target=self.poll_one.id,
            link_type=Poll,
            link_target=1,
            message='This is a poll message',
            date=datetime.datetime.now()
        )

        notification = notification_create(
            notification_type=Poll,
            notification_target=self.poll_one.id,
            link_type=Poll,
            link_target=1,
            message='This is a poll message',
            date=datetime.datetime.now()
        )

        notification = notification_create(
            notification_type=Group,
            notification_target=self.group_one.id,
            link_type=Poll,
            link_target=2,
            message='This is a poll message',
            date=datetime.datetime.now()
        )

    def test_list_notifications(self):
        url = reverse('notifications-list', kwargs=dict(type='poll'))
        self.client.force_login(self.user_one)
        response = self.client.get(url)
        print(response)

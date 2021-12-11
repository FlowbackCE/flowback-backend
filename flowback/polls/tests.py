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

from django.test import TestCase
from rest_framework import status
from flowback.polls.serializer import PollProposalCreateSerializer, PollProposalEventCreateSerializer, \
    PollProposalIndexCreateSerializer, PollProposalEventIndexCreateSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from flowback.polls.models import Poll, PollProposal, PollProposalThreads
from flowback.polls.views import GroupPollViewSet
import json
from django.urls import reverse
from flowback.users.models import User, Group
from rest_framework.test import APIClient, APITestCase

import datetime


# Default Test Case
class DefaultTestCase(TestCase):
    def setUp(self):
        # Create User
        user_one = dict(
            email='example@example.com',
            password='password123',
            accepted_terms_use=True,
            accepted_terms_condition=True
        )
        self.user_one = User.objects.create(**user_one)

        # Create Group
        group_one = dict(
            created_by=self.user_one,
            updated_by=self.user_one,
            title='Example Group',
            description='Example Description',
            public=True,
            members_request='direct_join',
            poll_approval='direct_approve',
            country='Sweden',
            city='Stockholm'
        )
        self.group_one = Group.objects.create(**group_one)

        # Create Poll
        poll_one = dict(
            created_by=self.user_one,
            modified_by=self.user_one,
            group=self.group_one,
            title="Example Poll",
            description="Example Description",
            type=Poll.Type.POLL,
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now() + datetime.timedelta(hours=1)
        )
        self.poll_one = Poll.objects.create(**poll_one)

        poll_two = dict(
            created_by=self.user_one,
            modified_by=self.user_one,
            group=self.group_one,
            title="Example Poll",
            description="Example Description",
            type=Poll.Type.EVENT,
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now() + datetime.timedelta(hours=1)
        )
        self.poll_two = Poll.objects.create(**poll_two)


# Create your tests here.
class Proposals(DefaultTestCase):
    def test_create_proposal_pass(self):
        counter_proposal_data = dict(
            poll=self.poll_one.id,
            proposal="Some proposal string",
            file=SimpleUploadedFile("file.txt", b"file_content", "text/plain")
        )

        proposal = PollProposalCreateSerializer(data=counter_proposal_data)
        proposal.is_valid(raise_exception=True)

    def test_create_proposal_event_fail(self):
        proposal_event_data = dict(
            poll=self.poll_one.id,
            proposal="Some proposal string",
            date=datetime.datetime.now() + datetime.timedelta(hours=1),
            file=SimpleUploadedFile("file.txt", b"file_content", "text/plain")
        )

        proposal_event = PollProposalEventCreateSerializer(data=proposal_event_data)
        if proposal_event.is_valid():
            self.fail('Event proposal created on Default Poll')

        self.assertEqual('Poll is not an Event.', proposal_event.errors['poll'][0])

    def test_create_proposal_event_fail_2(self):
        time = '09/19/18 13:55:01'
        proposal_event_data = dict(
            poll=self.poll_two.id,
            proposal="Some proposal string",
            date=datetime.datetime.strptime(time, '%m/%d/%y %H:%M:%S'),
            file=SimpleUploadedFile("file.txt", b"file_content", "text/plain")
        )

        proposal_event = PollProposalEventCreateSerializer(data=proposal_event_data)
        if proposal_event.is_valid():
            self.fail('Proposal Event Date passed outside of 5 minute increments')
        self.assertEqual(proposal_event.errors['date'][0], 'Date needs to be in 5 minute increments.')

    def test_create_proposal_event_pass(self):
        time = '09/19/18 13:55:00'
        proposal_event_data = dict(
            poll=self.poll_two.id,
            proposal="Some proposal string",
            date=datetime.datetime.strptime(time, '%m/%d/%y %H:%M:%S'),
            file=SimpleUploadedFile("file.txt", b"file_content", "text/plain")
        )

        proposal_event = PollProposalEventCreateSerializer(data=proposal_event_data)
        proposal_event.is_valid(raise_exception=True)


class TestBaseAPITestCase(APITestCase):
    def setUp(self):
        # Create User
        def generate_user(mail, passwd):
            user = dict(
                email=mail,
                username=mail,
                password=passwd,
                accepted_terms_use=True,
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

    def generate_index_proposals(self, user, positive, negative):
        x = len(positive + negative)
        data = []
        for proposal in positive:
            data.append(dict(
                proposal=proposal,
                user=user.id,
                priority=x,
                is_positive=True
            ))
            x -= 1

        for proposal in negative:
            data.append(dict(
                proposal=proposal,
                user=user.id,
                priority=x,
                is_positive=False
            ))
            x -= 1

        serializer = PollProposalIndexCreateSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


class TestGetProposals(TestBaseAPITestCase):
    def test_all_proposals(self):
        url = reverse("group_poll-all-proposals", args=[self.poll_one.id])

        self.client.force_login(self.user_one)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_user_proposal(self):
        url = reverse("group_poll-user-proposal", args=[self.poll_one.id])

        self.client.force_login(self.user_one)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['proposal'], 'some_1_proposal_0')
        self.assertEqual(response.data['user']['id'], self.user_one.id)

    def test_create_get_index_proposals(self):
        url = reverse("group_poll-update-index-proposals", args=[self.poll_one.id])
        self.client.force_login(self.user_one)
        data = {'positive': [3, 1], 'negative': [5]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {'positive': [4, 1], 'negative': [5]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse("group_poll-index-proposals", args=[self.poll_one.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['positive_proposals'] + response.data['negative_proposals']), 3)
        self.assertEqual(response.data['positive_proposals'][0]['id'], 3)
        self.assertEqual(response.data['negative_proposals'][0]['id'], 5)


from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from flowback.polls.models import Poll
from flowback.users.models import User, Group
from flowback.users.serializer import UserRegistrationSerializer

import datetime


# Create your tests here.
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


class UserTestCase(DefaultTestCase):
    def test_user_registration_serializer_fail(self):
        user_to_register = dict(
            email='placeholder@example.com',
            password='password123',
            accepted_terms_use=False,
            accepted_terms_condition=True
        )
        test = UserRegistrationSerializer(data=user_to_register)
        self.assertFalse(test.is_valid())

    def test_user_registration_serializer_pass(self):
        user_to_register = dict(
            email='placeholder@example.com',
            password='password123',
            accepted_terms_use=True,
            accepted_terms_condition=True
        )
        test = UserRegistrationSerializer(data=user_to_register)
        self.assertTrue(test.is_valid())

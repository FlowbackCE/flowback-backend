import datetime

import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.test import TestCase

from flowback.users.tests import UserFactory, GroupFactory

from flowback.polls.services import create_poll_receipt
from flowback.polls.helper import PollAdapter
from flowback.polls.models import Poll, PollProposal

class PollFactory(DjangoModelFactory):
    class Meta:
        model = Poll

    created_by = UserFactory.create()
    modified_by = created_by
    group = GroupFactory(created_by=created_by).create()
    title = factory.Faker('company')
    description = factory.Faker('bs')

    type = Poll.Type.POLL
    voting_type = Poll.VotingType.CONDORCET

    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now() + datetime.timedelta(days=1)


    # owner, member1, member2, member3 = [UserFactory.create() for x in range(4)]
    # group = GroupFactory(created_by=owner)
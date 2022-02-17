import datetime
import json
import random

import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.test import TestCase

from flowback.users.tests import UserFactory, GroupFactory

from flowback.polls.services import create_poll_receipt
from flowback.polls.helper import PollAdapter
from flowback.polls.models import Poll, PollProposal, PollProposalEvent, PollProposalIndex, PollProposalEventIndex


class PollFactory(DjangoModelFactory):
    class Meta:
        model = Poll

    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.LazyAttribute(lambda o: o.created_by)
    group = factory.SubFactory(GroupFactory, created_by=created_by)
    title = factory.Faker('company')
    description = factory.Faker('bs')

    type = Poll.Type.POLL
    voting_type = Poll.VotingType.CONDORCET

    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now() + datetime.timedelta(days=1)


class PollProposalFactory(DjangoModelFactory):
    class Meta:
        model = PollProposal

    user = factory.SubFactory(UserFactory)
    poll = factory.SubFactory(GroupFactory, created_by=user)
    type = PollProposal.Type.DEFAULT
    proposal = factory.Faker('bs')


class PollProposalEventFactory(DjangoModelFactory):
    class Meta:
        model = PollProposalEvent

    user = factory.SubFactory(UserFactory)
    poll = factory.SubFactory(GroupFactory, created_by=user)
    type = PollProposal.Type.DEFAULT
    proposal = factory.Faker('bs')
    date = datetime.datetime.now() + datetime.timedelta(hours=1)


class PollProposalIndexFactory(DjangoModelFactory):
    class Meta:
        model = PollProposalIndex

    user = factory.SubFactory(UserFactory)
    proposal = factory.SubFactory(PollProposalFactory, user=user)
    priority = 0
    is_positive = True


class PollProposalEventIndexFactory(DjangoModelFactory):
    class Meta:
        model = PollProposalEventIndex

    user = factory.SubFactory(UserFactory)
    proposal = factory.SubFactory(PollProposalEventFactory, user=user)
    priority = 0
    is_positive = True


class PollTestCase(TestCase):
    def test_create_poll_receipt(self):
        owner, member1, member2, member3, delegator1, delegator2 = UserFactory.create_batch(6)
        users = [owner, member1, member2, member3, delegator1, delegator2]
        group = GroupFactory(
            created_by=owner,
            owners=[owner],
            delegators=[delegator1, delegator2],
            members=[member1, member2, member3]
        )

        poll = PollFactory(created_by=owner, voting_type=Poll.VotingType.CARDINAL)

        proposal1, proposal2, proposal3 = [
            PollProposalFactory(poll=poll, user=user)
            for user in [member1, member2, member3]
        ]
        proposals = [proposal1, proposal2, proposal3]

        for user in users:
            for proposal in proposals:
                PollProposalIndexFactory(user=user, proposal=proposal, priority=random.randint(0, 2000))
        print(json.dumps(create_poll_receipt(poll=poll.id)))

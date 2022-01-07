import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.test import TestCase

from flowback.exceptions import PermissionDenied
from flowback.users.models import User, Group
from flowback.users.services import group_user_permitted, group_member_update

import datetime


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('first_name')
    email = factory.Faker('email')
    accepted_terms_condition = True


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    title = factory.Faker('company')
    created_by = UserFactory.create()
    updated_by = created_by


class UserTestCase(TestCase):
    def test_group_user_permitted(self):
        guest, member, delegator, moderator, admin, owner = [UserFactory.create() for x in range(6)]

        group = GroupFactory(created_by=owner, updated_by=owner)
        group.owners.add(owner)
        group.admins.add(admin)
        group.moderators.add(moderator)
        group.delegators.add(delegator)
        group.members.add(member)
        group.save()

        permissions = ['owner', 'admin', 'moderator', 'delegator', 'member', 'guest']
        member_permissions = ((owner, 0), (admin, 1), (moderator, 2), (delegator, 3),
                              (member, 3), (guest, 5))

        for user, perms in member_permissions:
            for permission in permissions[perms:]:
                self.assertTrue(group_user_permitted(
                    user=user,
                    group=group,
                    permission=permission
                    )
                )

            for permission in permissions[:perms]:
                self.assertFalse(group_user_permitted(
                    user=user,
                    group=group,
                    permission=permission,
                    raise_exception=False
                    )
                )

    def test_group_member_update(self):
        admin, member, user = [UserFactory.create() for x in range(3)]

        group = GroupFactory(created_by=admin, updated_by=admin)
        group.admins.add(admin)
        group.members.add(member)
        group.save()

        tests = [
            [admin, member, True, True],
            [admin, user, True, False],
            [member, admin, True, False],
            [admin, member, False, True],
            [admin, user, False, False],
            [member, admin, False, False]
        ]

        for user, target, allow_vote, passing in tests:
            if passing:
                self.assertTrue(group_member_update(
                    user=user,
                    target=target,
                    group=group,
                    allow_vote=allow_vote
                ))

            else:
                self.assertRaises(
                    PermissionDenied,
                    group_member_update,
                    user=user,
                    target=target,
                    group=group,
                    allow_vote=allow_vote
                )

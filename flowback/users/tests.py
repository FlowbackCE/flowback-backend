import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.test import TestCase
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

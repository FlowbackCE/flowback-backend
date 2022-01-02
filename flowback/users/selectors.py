from django.db.models import Q

from flowback.users.models import Group, User, GroupMembers


def get_group_member(*, user: User, group: Group) -> GroupMembers:
    query = Q(user=user, group=group)

    return GroupMembers.objects.get(query)


def get_group_members(*, group: Group):
    query = Q(group=group)

    return GroupMembers.objects.filter(query)

from django.db.models import Q

from flowback.users.models import Group, User, GroupMembers


def get_group_member(*, user: int, group: int) -> GroupMembers:
    query = Q(user_id=user, group_id=group)

    return GroupMembers.objects.get(query)


def get_group_members(*, group: int):
    query = Q(group_id=group)

    return GroupMembers.objects.filter(query)

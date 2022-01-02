from django.db.models import Q

from flowback.users.models import Group, User, GroupMembers


def get_group_user(*, user: User, group: Group) -> GroupMembers:
    query = Q(user=user, group=group)

    return GroupMembers.objects.get(query)

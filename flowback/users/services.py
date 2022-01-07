from django.db.models import Q
from django.shortcuts import get_object_or_404
from flowback.users.models import User, Group, GroupMembers
from flowback.exceptions import PermissionDenied
from django.core.exceptions import ValidationError


def group_user_permitted(
        *,
        user: int,
        group: int,
        permission: str,
        raise_exception: bool = True
) -> bool:
    user = get_object_or_404(User, id=user)
    group = get_object_or_404(Group, id=group)

    def public(is_public):
        return Q(public=is_public)

    owner = Q(owners__in=[user])
    admin = Q(admins__in=[user])
    moderator = Q(moderators__in=[user])
    delegator = Q(delegators__in=[user])
    member = Q(members__in=[user])

    permission_chart = dict(
        owner=Q(owner),
        admin=Q(owner | admin),
        moderator=Q(owner | admin | moderator),
        delegator=Q(owner | admin | moderator | delegator | member),
        member=Q(owner | admin | moderator | delegator | member),
        guest=public(True) | Q(owner | admin | moderator | delegator | member, public(False)),
    )

    if Group.objects.filter(permission_chart.get(permission), id=group.id).exists():
        return True

    elif raise_exception:
        raise PermissionDenied()

    else:
        return False


def group_member_update(
        *,
        user: int,
        target: int,
        group: int,
        allow_vote: bool = False
) -> bool:

    group_user_permitted(user=user, group=group, permission='admin')
    group_user_permitted(user=target, group=group, permission='member')
    GroupMembers.objects.update_or_create(
        user_id=target,
        group_id=group,
        defaults=dict(allow_vote=allow_vote)
    )
    return True

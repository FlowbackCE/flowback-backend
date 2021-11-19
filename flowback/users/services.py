from django.db.models import Q
from flowback.users.models import User, Group
from django.core.exceptions import ValidationError


def user_group_permitted(user: User, group_id: int):
    if Group.objects.filter(Q(owners__in=[user]) | Q(admins__in=[user]) |
                         Q(moderators__in=[user]) | Q(members__in=[user]) |
                         Q(delegators__in=[user]), id=group_id).exists():
        return True

    raise ValidationError('User is not in group')

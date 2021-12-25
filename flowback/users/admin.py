
from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from flowback.users.models import User, Group, OnboardUser, GroupRequest, Country, State, City


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = [

    ]
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    ]
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    ordering = ('email',)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'public')


class GroupRequestAdmin(admin.ModelAdmin):
    list_display = ('group', 'participant')


admin.site.register(Group, GroupAdmin)
admin.site.register(OnboardUser)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(GroupRequest, GroupRequestAdmin)

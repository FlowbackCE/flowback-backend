# FlowBack was created and project lead by Loke Hagberg. The design was
# made by Lina Forsberg. Emilio Müller helped constructing Flowback.
# Astroneatech created the code. It was primarily financed by David
# Madsen. It is a decision making platform.
# Copyright (C) 2021  Astroneatech AB
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/.

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

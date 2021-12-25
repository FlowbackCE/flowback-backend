
from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'flowback.users'

    def ready(self):
        import flowback.users.signals

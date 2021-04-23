from django.apps import AppConfig
from configparser import ConfigParser


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals


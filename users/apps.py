from django.apps import AppConfig
from configparser import ConfigParser


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        # from django.contrib.sites.models import Site
        # config = ConfigParser()
        # config.read('cst8333/config.properties')
        # print(config.sections())
        # print(config['DEFAULT']['title'])
        # print(config['domain']['host'])

        # rlcs_site = Sites.objects.all()
        # rlcs_site.domain = 'lange.ca'
        # rlcs.save()
        import users.signals


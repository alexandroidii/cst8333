from django.apps import AppConfig


class RlcisConfig(AppConfig):
    name = 'rlcis'

    def ready(self):
        import rlcis.signals


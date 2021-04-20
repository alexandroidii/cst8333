from django.apps import AppConfig

class RlcsConfig(AppConfig):
    name = 'rlcs'

    def ready(self):
        import rlcs.signals

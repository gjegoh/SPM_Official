from django.apps import AppConfig
from django.db.models.signals import post_migrate


class DbInitializerConfig(AppConfig):
    name = 'DB_init'

    def ready(self):
        from .signals import initial_web_app_group
        post_migrate.connect(initial_web_app_group, sender=self)
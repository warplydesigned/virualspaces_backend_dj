from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'virtualspaces.account'

    def ready(self):
        import virtualspaces.account.signals

from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals  # profile creation signals
        from django.contrib.auth.models import Group
        for role in ["Manager", "Purchaser"]:
            Group.objects.get_or_create(name=role)  # automatically create groups

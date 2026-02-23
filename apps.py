from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LeaveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leave'
    label = 'leave'
    verbose_name = _('Leave Management')

    def ready(self):
        pass

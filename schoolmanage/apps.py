from django.apps import AppConfig


class SchoolmanageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'schoolmanage'
    verbose_name = "Gestion de l'établissement"

    def ready(self):
        import schoolmanage.signals
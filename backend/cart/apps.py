from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
    verbose_name = 'Savatcha'

    def ready(self):
        import cart.signals  # noqa: F401 — signallarni ulash uchun import qilish kifoya

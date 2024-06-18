from django.apps import AppConfig


class OrderModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order_module'
    verbose_name = 'ماژول سبد خرید'

    # def ready(self):
    #     import order_module.signals  # وارد کردن سیگنال‌ها
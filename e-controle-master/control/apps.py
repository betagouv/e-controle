from django.apps import AppConfig


class ControlConfig(AppConfig):
    name = 'control'
    verbose_name = "Control"

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('ResponseFile'))
        registry.register(self.get_model('Question'))

from django.apps import AppConfig


class UserauthenticationConfig(AppConfig):
    name = 'userauthentication'
    
    def ready(self):
        import userauthentication.signals
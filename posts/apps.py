from django.apps import AppConfig

class PostsConfig(AppConfig):
    name = 'posts'
    def ready(self):
        from . import signals

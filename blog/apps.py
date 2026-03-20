from django.apps import AppConfig
from django.db.models.signals import post_migrate

class BlogConfig(AppConfig):
    name = 'blog'
    def ready(self):
        from blog.signals import create_group_permission
        post_migrate.connect(create_group_permission) 

from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_django.blog'

    def ready(self):
        import blog_django.blog.signals

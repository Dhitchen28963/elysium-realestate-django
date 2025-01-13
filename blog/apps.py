from django.apps import AppConfig

"""
Configures the 'blog' application settings, including the default auto
field type and the name of the app.
"""


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

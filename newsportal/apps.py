from django.apps import AppConfig
import redis

class NewsportalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsportal'

    def ready(self):
        import newsportal.signals

red = redis.Redis(
    host='redis-13999.c11.us-east-1-3.ec2.cloud.redislabs.com:13999',
    port=13999,
    password='KmnsMptFfo6EZjarJ0vNdwFH7WfsM8lr'
)


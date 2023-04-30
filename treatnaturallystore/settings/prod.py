import os
import dj_database_url
from .common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['treatnaturally-prod.herokuapp.com']


DATABASES = {
    'default': dj_database_url.config()
}

REDIS_URL = os.environ['REDIS_URL']

CELERY_BROKER_URL = REDIS_URL

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.treatnaturally.co.uk'
EMAIL_HOST_USER = 'noreply@treatnaturally.co.uk'
EMAIL_HOST_PASSWORD = os.environ['CPANEL_MAIL_PASSWORD']
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'noreply@treatnaturally.co.uk'



CORS_ORIGIN_ALLOW_ALL = True


CLOUDINARY_STORAGE = {
             'CLOUD_NAME': os.environ['CLOUD_NAME'],
             'API_KEY': os.environ['CLOUD_API_KEY'],
             'API_SECRET': os.environ['CLOUD_API_SECRET'],
            }

 
DEFAULT_FILE_STORAGE='cloudinary_storage.storage.MediaCloudinaryStorage'
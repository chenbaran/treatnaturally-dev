from .common import *
import stripe

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7w85$3#lasx-*ks8gflob($s=5ffe3z*ckbzu6h&-gi9wt_r+d'
STRIPE_PUBLIC_KEY = 'pk_test_51N2XnaKk6BdOIVOwcBnBmHRGup0aWEnalcBgHegTzWfzspVaNIbfqpEvDqctdHMmosBpYeQ5KxqHNNSWAejhvHnf00GLR1aAP3'
STRIPE_SECRET_KEY = 'sk_test_51N2XnaKk6BdOIVOwt9K0skhMXQAYokm07wtY0s9tY2DbZMODLA2TVmVTj7HZcgEmDjJYtdAQNn73AWb0tUohpf8200XaFuUIZZ'
WEBHOOK_SECRET_KEY = 'whsec_7993a062d5d590eb8c1785ebdf9591feb7ee7845e8fff6c1f776a6faae02ac56'

webhook_secret = WEBHOOK_SECRET_KEY
stripe.api_key = STRIPE_SECRET_KEY

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'treatnaturally_store',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'Femto1828##'
    }
}

CELERY_BROKER_URL = 'redis://redis:6379/1'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/2",
        "TIMEOUT": 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.treatnaturally.co.uk'
EMAIL_HOST_USER = 'noreply@treatnaturally.co.uk'
EMAIL_HOST_PASSWORD = ')6=nI7r#fowI'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'noreply@treatnaturally.co.uk'

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}

CORS_ORIGIN_ALLOW_ALL = True
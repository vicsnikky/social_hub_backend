from .base import *

SECRET_KEY = 'your-local-secret-key'
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'social_hub_db',
        'USER': 'postgres',
        'PASSWORD': 'alo13071996',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

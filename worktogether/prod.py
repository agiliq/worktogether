from .base import *


DATABASE_URL = os.environ.get('DATABASE_URL', '')
DB_NAME = DATABASE_URL.split('/')[-1]
DB_USER = os.environ.get('DB_USER', '')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_HOST = DATABASE_URL.split('@')[1].split(':')[0]

ALLOWED_HOSTS = ['worktracker.agiliq.com', '139.59.20.179', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '5432',
    }
}

INSTALLED_APPS += (
    'teamwork',
    'sendgrid_events',
)

EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

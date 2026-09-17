from .base import *
import dj_database_url
import os

DEBUG = False

raw_hosts = os.getenv('ALLOWED_HOST', '')
ALLOWED_HOSTS = [host.strip() for host in raw_hosts.split(',') if host.strip()]
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
]
for host in ALLOWED_HOSTS:
    if host != '*':
        CSRF_TRUSTED_ORIGINS.append(f'https://{host}')

SECRET_KEY = os.getenv('SECRET_KEY')
DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

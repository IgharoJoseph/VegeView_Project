from .base import *
import dj_database_url


DEBUG = os.getenv('DEBUG')
ALLOWED_HOSTS = os.getenv('HOST')
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
}


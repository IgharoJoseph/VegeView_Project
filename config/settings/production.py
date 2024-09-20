from .base import *
import dj_database_url
from dotenv import load_dotenv
load_dotenv()

DEBUG = False
# ALLOWED_HOSTS = os.getenv('ALLOWED_HOST','')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOST', '').split(',')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host.strip()]

SECRET_KEY = os.getenv('SECRET_KEY')
DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
}


import os

environment = os.getenv('DJANGO_ENV') or 'local'

if environment == 'production':
    from .prod import *
else:
    from .local import *

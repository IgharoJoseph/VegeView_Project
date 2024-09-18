import os

environment = os.getenv('DJANGO_ENV') or 'local'

if environment == 'production':
    from .production import *
    print('Production')
else:
    from .local import *
    print('Local Server')
    

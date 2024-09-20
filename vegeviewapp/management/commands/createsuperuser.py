from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
import os

class Command(createsuperuser.Command):
    help = 'Create a superuser, allowing for interactive input if environment variables are not set.'

    def handle(self, *args, **options):
        # Check for environment variables
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username:
            username = input("Username: ")
        if not email:
            email = input("Email: ")
        if not password:
            password = input("Password: ")

        # Now call the parent handle method
        options['username'] = username
        options['email'] = email
        options['password'] = password
        super().handle(*args, **options)

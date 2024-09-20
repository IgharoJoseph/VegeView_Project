import os
import logging
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

logger = logging.getLogger('vegeviewapp')

class Command(createsuperuser.Command):
    help = 'Create a superuser, and allow password to be provided from environment variables.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        logger.debug(f'Creating superuser with username: {username}, email: {email}')

        if not username or not email or not password:
            raise CommandError("Environment variables DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and DJANGO_SUPERUSER_PASSWORD must be set.")

        if options.get('preserve'):
            exists = self.UserModel._default_manager.filter(username=username).exists()
            if exists:
                logger.info("User exists, exiting normally due to --preserve")
                return

        super(Command, self).handle(*args, **options)

        user = self.UserModel._default_manager.get(username=username)
        user.email = email
        user.set_password(password)
        user.save()

        logger.debug(f'Superuser created: {user.username}, hashed password: {user.password}')

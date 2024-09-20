import logging
import os
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

logger = logging.getLogger(__name__)

class Command(createsuperuser.Command):
    help = 'Create a superuser, and allow password to be provided'

    def add_arguments(self, parser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        logger.debug(f"Username: {username}, Email: {email}, Password: {'*' * len(password) if password else None}")

        if not username or not password:
            logger.error("Username or password is missing from environment variables.")
            raise CommandError("Username and password must be set in environment variables.")

        # Check if the user already exists
        exists = self.UserModel._default_manager.filter(username=username).exists()
        if exists:
            logger.info(f"User '{username}' already exists.")
            return

        try:
            # Create superuser
            super().handle(*args, **options)

            # Set the password
            user = self.UserModel._default_manager.get(username=username)
            user.set_password(password)
            user.save()

            logger.info(f"Superuser '{username}' created successfully.")
        except Exception as e:
            logger.exception("Failed to create superuser.")
            raise CommandError("An error occurred while creating the superuser.")


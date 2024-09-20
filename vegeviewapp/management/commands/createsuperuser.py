import os
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

class Command(createsuperuser.Command):
    help = 'Create a superuser using environment variables'

    def add_arguments(self, parser):
        parser.add_argument('--no-input', action='store_true', help='Avoid prompting for input')

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username:
            raise CommandError("DJANGO_SUPERUSER_USERNAME environment variable is required.")
        if not password:
            raise CommandError("DJANGO_SUPERUSER_PASSWORD environment variable is required.")

        # Check if the user already exists
        if self.UserModel._default_manager.filter(username=username).exists():
            self.stdout.write(f"User '{username}' already exists.")
            return

        # Create the superuser without input prompts
        super().handle(*args, **options)

        user = self.UserModel._default_manager.get(username=username)
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))

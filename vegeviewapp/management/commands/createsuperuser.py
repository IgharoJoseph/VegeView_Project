# management/commands/createsuperuser.py

from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from django.conf import settings

class Command(createsuperuser.Command):
    help = 'Create a superuser, allowing password to be provided from environment variables'

    def handle(self):
        username = settings.DJANGO_SUPERUSER_USERNAME
        email = settings.DJANGO_SUPERUSER_EMAIL
        password = settings.DJANGO_SUPERUSER_PASSWORD

        if not username or not password:
            raise CommandError("--username and --password are required.")

        user, created = self.UserModel._default_manager.get_or_create(
            username=username,
            defaults={
                'email': email,
            }
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {username} already exists.'))

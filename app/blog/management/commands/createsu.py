from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Creates a superuser'

    def handle(self, *args, **options):
        username = os.getenv('ADM_LOGIN', 'admin')
        email = os.getenv('ADM_EMAIL', 'admin@example.com')
        password = os.getenv('ADM_PASSWORD', 'adminpassword')
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {username} already exists.'))

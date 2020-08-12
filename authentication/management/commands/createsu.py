from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="admin@example.com").exists():
            User.objects.create_superuser("admin@example.com", "admin@123", "admin")
            self.stdout.write(self.style.SUCCESS('Successfully created new super user'))
        else:
            self.stdout.write(self.style.SUCCESS('user already exist'))

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running migrations...'))
        call_command('migrate')  # Run migrations
        self.stdout.write(self.style.SUCCESS('Migrations completed.'))

        User = get_user_model()
        username = "Rubesh"
        email = 'rubeshchander.rc@gmail.com'
        password = 'ruby123'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(
                f'Superuser {username} created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Superuser {username} already exists.'))

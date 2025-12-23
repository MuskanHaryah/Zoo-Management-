from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a caretaker user for testing'

    def handle(self, *args, **options):
        username = 'jack_caretaker'
        password = 'zoo12345'
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User {username} already exists!'))
            return
        
        # Create the user
        User.objects.create_user(username=username, password=password)
        self.stdout.write(self.style.SUCCESS(f'Successfully created user {username} with password {password}'))

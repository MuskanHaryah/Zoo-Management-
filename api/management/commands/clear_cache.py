from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Clear all Django cache'

    def handle(self, *args, **options):
        # Clear Django's cache
        cache.clear()
        self.stdout.write("Successfully cleared Django cache")
        
        # Provide instructions for browser cache clearing
        self.stdout.write(
            "\nIMPORTANT: You also need to clear your browser cache:"
            "\n1. Press Ctrl+F5 or Shift+F5 in most browsers"
            "\n2. Or use the browser's developer tools to disable cache"
            "\n3. Or clear browser history/cache from browser settings"
        )

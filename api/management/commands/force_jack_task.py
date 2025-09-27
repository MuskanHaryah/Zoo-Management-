from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Task, Animal

class Command(BaseCommand):
    help = 'Force update the specific task for Jack to rejected status'

    def handle(self, *args, **options):
        now = timezone.now()
        self.stdout.write(f"Current time: {now}")
        
        # Try to find Jack's task
        try:
            # Look for Jack's task in multiple ways to ensure we find it
            tasks = Task.objects.filter(animal__name__icontains='jack')
            
            if not tasks.exists():
                self.stdout.write("No tasks found for Jack by name, trying by description")
                tasks = Task.objects.filter(description__icontains='feed him')
            
            if not tasks.exists():
                self.stdout.write("No tasks found by description either, listing all tasks:")
                tasks = Task.objects.all()
                for t in tasks:
                    self.stdout.write(f"ID: {t.id}, Animal: {t.animal.name}, Status: {t.status}, Description: {t.description}")
                return
            
            for task in tasks:
                self.stdout.write(f"Found task ID: {task.id} for {task.animal.name}")
                self.stdout.write(f"Current status: {task.status}")
                self.stdout.write(f"Deadline: {task.deadline}")
                self.stdout.write(f"Current time vs deadline: {now > task.deadline if task.deadline else 'No deadline'}")
                
                # Force update to rejected regardless
                task.status = 'rejected'
                task.save()
                
                # Verify the change
                task.refresh_from_db()
                self.stdout.write(f"Updated status: {task.status}")
        
        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")

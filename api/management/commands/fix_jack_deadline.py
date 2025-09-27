from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Task, Animal
from datetime import datetime

class Command(BaseCommand):
    help = 'Fix the deadline date for Jack\'s tasks to match the UI'

    def handle(self, *args, **options):
        now = timezone.now()
        self.stdout.write(f"Current time: {now}")
        
        # Find Jack's tasks
        tasks = Task.objects.filter(animal__name__icontains='jack')
        
        for task in tasks:
            self.stdout.write(f"Found task ID: {task.id} for {task.animal.name}")
            self.stdout.write(f"Current status: {task.status}")
            self.stdout.write(f"Current deadline: {task.deadline}")
            
            # Set deadline to April 12, 2025, midnight
            from django.utils.timezone import make_aware
            new_deadline = make_aware(datetime(2025, 4, 12, 0, 0, 0))
            
            # Update the deadline
            task.deadline = new_deadline
            task.save()
            
            # Verify the change
            task.refresh_from_db()
            self.stdout.write(f"Updated deadline: {task.deadline}")
            
            # Ensure status is rejected since this date is now in the past
            if task.deadline and now > task.deadline and task.status.lower() != 'rejected':
                task.status = 'rejected'
                task.save()
                self.stdout.write(f"Also updated status to: {task.status}")

from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Task
from datetime import datetime

class Command(BaseCommand):
    help = 'Updates the task deadline to a past date for testing'

    def handle(self, *args, **options):
        try:
            task = Task.objects.get(description__icontains='feed him')
            
            # Set deadline to April 12, 2025
            new_deadline = datetime(2025, 4, 12, 12, 0)
            task.deadline = new_deadline
            task.status = 'pending'  # Reset status to pending
            task.save()
            
            self.stdout.write(f"Updated task {task.id} deadline to {new_deadline} and reset status to pending")
            
            # Verify the change
            task.refresh_from_db()
            self.stdout.write(f"Task details after update: status={task.status}, deadline={task.deadline}")
            
            # Check if it would now be considered expired
            now = timezone.now()
            is_expired = now > task.deadline
            self.stdout.write(f"Current time: {now}")
            self.stdout.write(f"Is deadline passed now? {is_expired}")
            
        except Task.DoesNotExist:
            self.stdout.write("Task with description 'feed him' not found")
        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")

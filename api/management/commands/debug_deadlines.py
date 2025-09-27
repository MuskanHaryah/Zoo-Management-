from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Task
import datetime

class Command(BaseCommand):
    help = 'Debug task deadlines'

    def handle(self, *args, **options):
        # Get current time
        now = timezone.now()
        self.stdout.write(f"Current time (timezone.now): {now}")
        self.stdout.write(f"Current time (naive): {datetime.datetime.now()}")
        self.stdout.write(f"Time zone active: {timezone.is_aware(now)}\n")
        
        # Get all tasks and check their deadlines
        tasks = Task.objects.all()
        self.stdout.write(f"Total tasks: {tasks.count()}")
        
        for task in tasks:
            self.stdout.write(f"\nTask ID: {task.id}")
            self.stdout.write(f"Description: {task.description}")
            self.stdout.write(f"Current status: {task.status}")
            self.stdout.write(f"Deadline: {task.deadline}")
            
            if task.deadline:
                is_timezone_aware = timezone.is_aware(task.deadline)
                self.stdout.write(f"Deadline timezone aware: {is_timezone_aware}")
                
                # Ensure both times are timezone-aware for comparison
                deadline = task.deadline
                if not is_timezone_aware:
                    deadline = timezone.make_aware(deadline)
                
                is_past_deadline = now > deadline
                self.stdout.write(f"Is past deadline: {is_past_deadline}")
                
                # Update the task if needed
                if task.status == 'pending' and is_past_deadline:
                    task.status = 'rejected'
                    task.save()
                    self.stdout.write(f"Updated task status to: {task.status}")
            else:
                self.stdout.write("No deadline set for this task")

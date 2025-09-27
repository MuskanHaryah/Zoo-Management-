from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Task

class Command(BaseCommand):
    help = 'Forcibly updates a specific task status regardless of current checks'

    def handle(self, *args, **options):
        now = timezone.now()
        self.stdout.write(f"Current time: {now}")
        
        # Find the specific task by its description and check its deadline
        try:
            task = Task.objects.get(description__icontains='feed him')
            self.stdout.write(f"Found task: {task.id}")
            self.stdout.write(f"Task details: status={task.status}, deadline={task.deadline}")
            
            if task.deadline:
                is_expired = now > task.deadline
                self.stdout.write(f"Is deadline passed? {is_expired}")
                
                # Force update the task
                task.status = 'rejected'
                task.save()
                self.stdout.write(f"Forcibly updated task status to: {task.status}")
            else:
                self.stdout.write("Task has no deadline set")
        except Task.DoesNotExist:
            self.stdout.write("Task with description 'feed him' not found")
        except Task.MultipleObjectsReturned:
            tasks = Task.objects.filter(description__icontains='feed him')
            self.stdout.write(f"Multiple tasks found ({tasks.count()}):")
            for t in tasks:
                self.stdout.write(f"Task {t.id}: status={t.status}, deadline={t.deadline}")
                t.status = 'rejected'
                t.save()
                self.stdout.write(f"Updated task {t.id} status to: {t.status}")

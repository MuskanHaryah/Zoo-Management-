from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Task

class Command(BaseCommand):
    help = 'Checks for expired tasks and marks them as rejected'

    def handle(self, *args, **options):
        now = timezone.now()
        
        # Find all pending tasks with deadlines in the past
        expired_tasks = Task.objects.filter(
            status='pending',
            deadline__lt=now,
            deadline__isnull=False
        )
        
        self.stdout.write(f"Current time: {now}")
        
        # Show all tasks for debugging
        all_tasks = Task.objects.all()
        self.stdout.write(f"All tasks in system: {all_tasks.count()}")
        for task in all_tasks:
            self.stdout.write(f"Task {task.id}: status={task.status}, deadline={task.deadline}, " +
                             f"is_expired={bool(task.deadline and now > task.deadline)}")
        
        # Update tasks
        count = 0
        for task in expired_tasks:
            self.stdout.write(f"Marking task {task.id} as rejected. Deadline was {task.deadline}")
            task.status = 'rejected'
            task.save()
            count += 1
        
        self.stdout.write(f"Updated {count} expired tasks to 'rejected' status")

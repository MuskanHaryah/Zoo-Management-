from django.core.management.base import BaseCommand
from api.models import Task
from django.contrib.admin.models import LogEntry

class Command(BaseCommand):
    help = 'Debug admin UI task display issues'

    def handle(self, *args, **options):
        # Check for tasks in the database
        tasks = Task.objects.all()
        self.stdout.write(f"Found {tasks.count()} tasks in database")
        
        # Look specifically for the task with Jack
        jack_tasks = Task.objects.filter(animal__name__icontains='jack')
        self.stdout.write(f"Found {jack_tasks.count()} tasks for Jack")
        
        # Print details of all tasks
        self.stdout.write("\nTask details:")
        for task in tasks:
            self.stdout.write(f"ID: {task.id}, Animal: {task.animal.name}, " +
                             f"Status: '{task.status}', Deadline: {task.deadline}")
            
        # Check for any admin log entries related to Jack's task
        if jack_tasks.exists():
            task_ids = [t.id for t in jack_tasks]
            log_entries = LogEntry.objects.filter(
                content_type__model='task',
                object_id__in=[str(id) for id in task_ids]
            ).order_by('-action_time')
            
            self.stdout.write("\nAdmin log entries for Jack's tasks:")
            for entry in log_entries:
                self.stdout.write(f"Time: {entry.action_time}, " +
                                 f"Action: {entry.get_action_flag_display()}, " +
                                 f"Message: {entry.get_change_message()}")

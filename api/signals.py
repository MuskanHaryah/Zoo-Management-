from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@receiver(post_migrate)
def create_check_expired_tasks_cron(sender, **kwargs):
    """Set up a periodic task to check for expired tasks after migrations"""
    try:
        # Only run this if we're using Celery
        if 'django_celery_beat' in settings.INSTALLED_APPS:
            from django_celery_beat.models import PeriodicTask, IntervalSchedule
            
            # Create or get the hourly schedule
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.HOURS,
            )
            
            # Create the periodic task if it doesn't exist
            task_name = 'Check expired tasks'
            PeriodicTask.objects.get_or_create(
                name=task_name,
                defaults={
                    'interval': schedule,
                    'task': 'api.tasks.check_expired_tasks_task',
                    'enabled': True,
                }
            )
            
            if created:
                logger.info(f"Created periodic task '{task_name}'")
            else:
                logger.info(f"Periodic task '{task_name}' already exists")
    except Exception as e:
        logger.error(f"Failed to create periodic task: {e}")

# Alternative method using signals to check tasks on each request
from django.core.signals import request_started

@receiver(request_started)
def check_expired_tasks_on_request(sender, **kwargs):
    """Check for expired tasks on each request"""
    from .views import check_expired_tasks
    
    # Only run this check occasionally to reduce database load
    # e.g., with a 5% chance on each request
    import random
    if random.random() < 0.05:  # 5% chance
        try:
            count = check_expired_tasks()
            if count > 0:
                logger.info(f"Updated {count} expired tasks to 'rejected' status")
        except Exception as e:
            logger.error(f"Error checking expired tasks: {e}")

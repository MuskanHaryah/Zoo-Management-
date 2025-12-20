from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Celery periodic task setup is disabled
# Use management commands or external cron jobs for periodic task checking
# Example: python manage.py check_expired_tasks
# @receiver(request_started)
# def check_expired_tasks_on_request(sender, **kwargs):
#     """Check for expired tasks on each request"""
#     from .views import check_expired_tasks
#     import random
#     
#     # Only run this check occasionally to reduce database load
#     # e.g., with a 5% chance on each request
#     if random.random() < 0.05:  # 5% chance
#         try:
#             count = check_expired_tasks()
#             if count > 0:
#                 logger.info(f"Updated {count} expired tasks to 'rejected' status")
#         except Exception as e:
#             logger.error(f"Error checking expired tasks: {e}")


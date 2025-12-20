from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import CaretakerProfile, Task, Animal
import json

@login_required(login_url='/caretaker/login/')
def caretaker_profile(request):
    try:
        caretaker = CaretakerProfile.objects.select_related('user').get(user=request.user)
        
        # Optimize query with select_related to prevent N+1 queries
        tasks = Task.objects.filter(caretaker=caretaker).select_related('animal', 'caretaker__user')
        
        # Update expired tasks in bulk (more efficient)
        from django.utils import timezone
        now = timezone.now()
        Task.objects.filter(
            caretaker=caretaker,
            status='pending',
            deadline__lt=now,
            deadline__isnull=False
        ).update(status='rejected')
        
        # Refresh the task list after updates
        tasks = Task.objects.filter(caretaker=caretaker).select_related('animal', 'caretaker__user')
        
        return render(request, 'caretaker/profile.html', {'tasks': tasks})
    except CaretakerProfile.DoesNotExist:
        # User is logged in but doesn't have a caretaker profile
        from django.contrib import messages
        messages.error(request, 'Your account is not associated with a caretaker profile. Please contact the administrator.')
        return redirect('caretaker_login')
    except Exception as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in caretaker_profile: {str(e)}")
        # Show user-friendly error message
        from django.contrib import messages
        messages.error(request, 'An unexpected error occurred. Please try again or contact support.')
        return redirect('landing_page')

@login_required(login_url='/caretaker/login/')
@require_POST

@login_required(login_url='/caretaker/login/')
@require_POST
def complete_task(request, task_id):
    try:
        # Get the task and verify it belongs to the current caretaker (optimized query)
        caretaker = CaretakerProfile.objects.select_related('user').get(user=request.user)
        task = get_object_or_404(
            Task.objects.select_related('animal', 'caretaker'),
            id=task_id, 
            caretaker=caretaker
        )
        
        # Update task status and submission date - use full datetime
        task.status = 'completed'
        task.submission_date = timezone.now()  # Use full datetime not just date
        task.save(update_fields=['status', 'submission_date'])
        
        return JsonResponse({
            'success': True, 
            'message': f'Task for {task.animal.name} marked as completed successfully!'
        })
    except CaretakerProfile.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'message': 'Your caretaker profile was not found. Please contact the administrator.'
        }, status=403)
    except Exception as e:
        # Log the error
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error completing task {task_id}: {str(e)}")
        
        return JsonResponse({
            'success': False, 
            'message': 'Unable to complete the task. Please try again or contact support if the problem persists.'
        }, status=500)

@login_required(login_url='/caretaker/login/')
def task_detail(request, task_id):
    """API endpoint to get task details"""
    try:
        caretaker = CaretakerProfile.objects.select_related('user').get(user=request.user)
        task = get_object_or_404(
            Task.objects.select_related('animal', 'caretaker'),
            id=task_id, 
            caretaker=caretaker
        )
        
        # Handle deadline - if it's None, explicitly set to None for JSON
        deadline = task.deadline.isoformat() if task.deadline else None
        
        # Return task details as JSON
        return JsonResponse({
            'id': task.id,
            'description': task.description,
            'status': task.status,
            'date_assigned': task.date_assigned.isoformat(),
            'deadline': deadline,  # Explicitly handle null case
            'animal': {
                'id': task.animal.id,
                'name': task.animal.name,
            }
        })
    except CaretakerProfile.DoesNotExist:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@login_required(login_url='/caretaker/login/')
def rejected_tasks(request):
    """API endpoint to get all rejected tasks for the current caretaker"""
    try:
        caretaker = CaretakerProfile.objects.select_related('user').get(user=request.user)
        tasks = Task.objects.filter(caretaker=caretaker, status='rejected').select_related('animal', 'caretaker')
        
        # Prepare JSON response with task data
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                'id': task.id,
                'description': task.description,
                'date_assigned': task.date_assigned.isoformat(),
                'submission_date': task.submission_date.isoformat() if task.submission_date else None,
                'rejection_date': task.rejection_date.isoformat() if hasattr(task, 'rejection_date') and task.rejection_date else None,
                'rejection_reason': task.rejection_reason if hasattr(task, 'rejection_reason') else None,
                'animal': {
                    'id': task.animal.id,
                    'name': task.animal.name,
                }
            })
        
        return JsonResponse(tasks_data, safe=False)
    except CaretakerProfile.DoesNotExist:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

# Duplicate complete_task function removed - using the one above with @require_POST decorator


def landing_page(request):
    """View for the landing page that directs users to visitor or caretaker sections"""
    response = render(request, 'caretaker/landing.html')
    # Add cache control headers to prevent caching
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Add this function to your views.py file

def visitor_page(request):
    """View for the visitor page showing zoo information and ticket booking"""
    return render(request, 'visitor/visitor.html')


def check_expired_tasks():
    """
    Utility function to check all tasks in the system for expired deadlines
    Can be called by a scheduled task runner like Celery or Django's management command
    """
    from django.utils import timezone
    now = timezone.now()
    
    # Find all pending tasks with deadlines in the past
    # Using __iexact for case-insensitive matching
    expired_tasks = Task.objects.filter(
        status__iexact='pending',
        deadline__lt=now,  # Less than current time
        deadline__isnull=False  # Only check tasks that have deadlines
    )
    
    # Update all expired tasks to rejected status
    count = expired_tasks.update(status='rejected')
    
    return count  # Return the number of tasks that were updated
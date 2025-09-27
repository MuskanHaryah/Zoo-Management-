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
        caretaker = CaretakerProfile.objects.get(user=request.user)
        # Get all tasks for this caretaker
        tasks = Task.objects.filter(caretaker=caretaker)
        
        # Check for tasks with passed deadlines and update their status
        for task in tasks:
            # Use the model method to check and update status
            if task.check_and_update_expired_status():
                print(f"Task {task.id} with deadline {task.deadline} was automatically rejected")
        
        # Refresh the task list after potential updates
        tasks = Task.objects.filter(caretaker=caretaker)
        return render(request, 'caretaker/profile.html', {'tasks': tasks})
    except CaretakerProfile.DoesNotExist:
        return redirect('caretaker_login')  # or show error

@login_required(login_url='/caretaker/login/')
@require_POST

@login_required(login_url='/caretaker/login/')
@require_POST
def complete_task(request, task_id):
    try:
        # Get the task and verify it belongs to the current caretaker
        caretaker = CaretakerProfile.objects.get(user=request.user)
        task = get_object_or_404(Task, id=task_id, caretaker=caretaker)
        
        # Update task status and submission date - use full datetime
        task.status = 'completed'
        task.submission_date = timezone.now()  # Use full datetime not just date
        task.save()
        
        return JsonResponse({'success': True, 'message': 'Task marked as completed'})
    except CaretakerProfile.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Caretaker profile not found'}, status=403)
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required(login_url='/caretaker/login/')
def task_detail(request, task_id):
    """API endpoint to get task details"""
    try:
        caretaker = CaretakerProfile.objects.get(user=request.user)
        task = get_object_or_404(Task, id=task_id, caretaker=caretaker)
        
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
        caretaker = CaretakerProfile.objects.get(user=request.user)
        tasks = Task.objects.filter(caretaker=caretaker, status='rejected')
        
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
    

@login_required
def complete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        
        # Find the caretaker profile associated with the current user
        try:
            caretaker_profile = CaretakerProfile.objects.get(user=request.user)
            
            # Check if this task belongs to the current caretaker
            if task.caretaker == caretaker_profile:
                try:
                    # Parse request data
                    data = json.loads(request.body.decode('utf-8'))
                    submission_date = data.get('submission_date')
                    
                    # Update task status - use lowercase to match STATUS_CHOICES in model
                    task.status = 'completed'
                    
                    # Save submission date
                    if submission_date:
                        from django.utils.dateparse import parse_datetime
                        task.submission_date = parse_datetime(submission_date)
                    else:
                        from django.utils import timezone
                        task.submission_date = timezone.now()
                        
                    task.save()
                    
                    return JsonResponse({'status': 'success'})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            else:
                return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
                
        except CaretakerProfile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User is not a caretaker'}, status=403)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


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
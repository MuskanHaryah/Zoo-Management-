from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import CaretakerProfile, Task

@login_required(login_url='/caretaker/login/')
def caretaker_profile(request):
    try:
        caretaker = CaretakerProfile.objects.get(user=request.user)
        tasks = Task.objects.filter(caretaker=caretaker)
        return render(request, 'caretaker/profile.html', {'tasks': tasks})
    except CaretakerProfile.DoesNotExist:
        return redirect('caretaker_login')  # or show error

@login_required(login_url='/caretaker/login/')
@require_POST
def mark_task_done(request, task_id):
    try:
        # Get the task and verify it belongs to the current caretaker
        caretaker = CaretakerProfile.objects.get(user=request.user)
        task = get_object_or_404(Task, id=task_id, caretaker=caretaker)
        
        # Update task status and submission date
        task.status = 'completed'
        task.submission_date = timezone.now().date()
        task.save()
        
        return JsonResponse({'success': True, 'message': 'Task marked as completed'})
    except CaretakerProfile.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Caretaker profile not found'}, status=403)
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

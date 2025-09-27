from django.urls import path
from . import views

urlpatterns = [
    path('caretaker/profile/', views.caretaker_profile, name='caretaker_profile'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('tasks/rejected/', views.rejected_tasks, name='rejected_tasks'),
    # Add this to your urlpatterns list
     path('', views.landing_page, name='landing_page'),
    path('visitor/', views.visitor_page, name='visitor_page'),
]


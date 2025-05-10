from django.urls import path
from . import views

urlpatterns = [
    path('caretaker/profile/', views.caretaker_profile, name='caretaker_profile'),

]

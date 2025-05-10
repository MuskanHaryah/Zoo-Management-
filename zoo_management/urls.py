from django.contrib import admin
from django.urls import path, include
from api.models import admin_site
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin URLs
    path('admin/', admin_site.urls),

    # Caretaker Authentication URLs
    path('caretaker/login/', auth_views.LoginView.as_view(
        template_name='caretaker/login.html'
    ), name='caretaker_login'),
    
    path('caretaker/logout/', auth_views.LogoutView.as_view(
        next_page='caretaker_login'
    ), name='caretaker_logout'),

    # Include API URLs
    path('', include('api.urls')),
]
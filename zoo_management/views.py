"""
Custom error handlers for Zoo Management System
"""
from django.shortcuts import render


def custom_403(request, exception):
    """
    Custom 403 error handler
    Shows user-friendly page when access is forbidden
    """
    return render(request, '403.html', status=403)


def custom_404(request, exception):
    """
    Custom 404 error handler
    Shows user-friendly page when resource is not found
    """
    return render(request, '404.html', status=404)


def custom_500(request):
    """
    Custom 500 error handler
    Shows user-friendly page when server error occurs
    """
    return render(request, '500.html', status=500)

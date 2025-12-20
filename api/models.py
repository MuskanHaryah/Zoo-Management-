from django.db import models
from django.contrib.auth.models import User  # Using the built-in User model
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField
from django.contrib.admin import AdminSite


class MyAdminSite(AdminSite):
    site_header = "ZOO Admin Panel"
    site_title = "ZOO Admin"
    index_title = "Welcome to Zoo Management"

    # Optional override — now shows ALL apps user has permission for
    def get_app_list(self, request):
        return super().get_app_list(request)
# Create an instance of your custom admin site
admin_site = MyAdminSite(name='myadmin')



# Caretaker Profile (optional extension for caretakers)
class CaretakerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phoneNo = models.CharField(max_length=15)
    address = models.TextField()
    shiftTime = models.CharField(max_length=50)

    def __str__(self):
        return f"Caretaker: {self.user.username}"


# Animal Model
class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    weight = models.FloatField()
    health_info = models.TextField()
    locationInZoo = models.CharField(max_length=100)
    caretaker = models.OneToOneField(CaretakerProfile, on_delete=models.SET_NULL, null=True)
    from django.db import models
    image = CloudinaryField('image', folder='Animals')
 



    def __str__(self):
        return f"{self.name} ({self.species})"


# Event Model
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = CloudinaryField('image', folder='Events/images', blank=True, null=True)
    video = CloudinaryField('video', folder='Events/videos', blank=True, null=True)
    date = models.DateTimeField()
    max_capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.title


# Booking Model
class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_count = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='confirmed')  # Or 'cancelled'

    def __str__(self):
        return f"{self.user.username} → {self.event.title}"


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    caretaker = models.ForeignKey(CaretakerProfile, on_delete=models.SET_NULL, null=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    description = models.TextField()
    date_assigned = models.DateTimeField(auto_now_add=True)  # Changed to DateTimeField
    deadline = models.DateTimeField(null=True, blank=True)  # Added deadline field
    submission_date = models.DateTimeField(null=True, blank=True)  # Changed to DateTimeField
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        indexes = [
            models.Index(fields=['status', 'deadline']),
            models.Index(fields=['caretaker', 'status']),
            models.Index(fields=['-date_assigned']),
        ]
        ordering = ['-date_assigned']

    def __str__(self):
        return f"Task for {self.animal.name} by {self.caretaker.user.username}"
    
    def is_past_deadline(self):
        """Check if the task is past its deadline"""
        from django.utils import timezone
        if self.deadline and timezone.now() > self.deadline:
            return True
        return False
        
    def check_and_update_expired_status(self):
        """Check if task is past deadline and update status if needed"""
        if self.is_past_deadline() and self.status.lower() == 'pending':
            self.status = 'rejected'
            self.save()
            return True
        return False




# Content Model
class Content(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('article', 'Article'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)  # For article type
    media = CloudinaryField('media', folder='Content for Visitor', blank=True, null=True)  # For image/video
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Wildlife Fact Model
class WildlifeFact(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    fact_text = models.TextField()

    def __str__(self):
        return f"Fact about {self.animal.name}"

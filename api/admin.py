from django.contrib import admin
from .models import admin_site
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin



from .models import (
    CaretakerProfile,
    Animal,
    Event,
    Booking,
    Task,
    Content,
    WildlifeFact
)
    
class CaretakerProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phoneNo', 'shiftTime')

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'age','gender', 'locationInZoo', 'caretaker')

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'max_capacity')

class BookingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False  # Disable "Add"

    def has_delete_permission(self, request, obj=None):
        return True  # Optional: Admin can still delete

class TaskAdmin(admin.ModelAdmin):
    list_display = ('caretaker', 'animal', 'status', 'date_assigned', 'submission_date')
    list_filter = ('status',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "caretaker":
            kwargs["queryset"] = CaretakerProfile.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'created_at')
    list_filter = ('media_type',)

class WildlifeFactAdmin(admin.ModelAdmin):
    list_display = ('animal', 'fact_text')

# ✅ Register all with your custom admin_site instead of the default one
admin_site.register(CaretakerProfile, CaretakerProfileAdmin)
admin_site.register(Animal, AnimalAdmin)
admin_site.register(Event, EventAdmin)
admin_site.register(Booking, BookingAdmin)
admin_site.register(Task, TaskAdmin)
admin_site.register(Content, ContentAdmin)
admin_site.register(WildlifeFact, WildlifeFactAdmin)
# Register built-in auth models to your custom admin site
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
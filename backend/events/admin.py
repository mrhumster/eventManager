from django.contrib import admin

from events.models import Event, Guest


# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    model = Guest
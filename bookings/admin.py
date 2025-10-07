from django.contrib import admin
from .models import Venue, Booking

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "capacity", "city")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "venue", "customer_name", "start_time", "end_time", "status")
    list_filter = ("status", "venue")

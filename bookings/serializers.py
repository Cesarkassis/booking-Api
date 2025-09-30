# bookings/serializers.py
from rest_framework import serializers
from .models import Venue, Booking

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = "__all__"
class BookingSerializer(serializers.ModelSerializer):
    venue = serializers.PrimaryKeyRelatedField(queryset=Venue.objects.all())

    class Meta:
        model = Booking
        fields = ["id", "venue", "customer_name", "customer_email", "start_time", "end_time", "status", "created_at"]
        read_only_fields = ["created_at", "status"]

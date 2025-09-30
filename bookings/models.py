from django.db import models

# Create your models here.# bookings/models.py

class Venue(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    capacity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="venues/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.city})"


class Booking(models.Model):
    venue = models.ForeignKey(Venue, related_name="bookings", on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="CONFIRMED")

    def __str__(self):
        return f"Booking {self.id} at {self.venue.name} for {self.customer_name}"


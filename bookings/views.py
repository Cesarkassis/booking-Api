from django.shortcuts import render

# Create your views here.
# bookings/views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Venue, Booking
from .serializers import VenueSerializer, BookingSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Venue, Booking
from .serializers import VenueSerializer, BookingSerializer

class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

    # Custom endpoint: /venues/findByCity?city=Paris
    @action(detail=False, methods=["get"])
    def findByCity(self, request):
        city = request.query_params.get("city")
        venues = Venue.objects.filter(city__iexact=city) if city else Venue.objects.all()
        serializer = self.get_serializer(venues, many=True)
        return Response(serializer.data)

    # Custom endpoint: /venues/{id}/availability
    @action(detail=True, methods=["get"])
    def availability(self, request, pk=None):
        venue = self.get_object()
        bookings = Booking.objects.filter(venue=venue, status="active")
        return Response({
            "venue": venue.name,
            "city": venue.city,
            "capacity": venue.capacity,
            "active_bookings": bookings.count(),
            "available": venue.capacity - bookings.count()
        })

    # Custom endpoint: /venues/{id}/uploadImage
    @action(detail=True, methods=["post"])
    def uploadImage(self, request, pk=None):
        venue = self.get_object()
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded"}, status=400)
        venue.image = file
        venue.save()
        return Response({"status": "Image uploaded", "venue": venue.name})

    # Custom endpoint: /venues/{id}/bookings
    @action(detail=True, methods=["get"])
    def bookings(self, request, pk=None):
        venue = self.get_object()
        bookings = Booking.objects.filter(venue=venue)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)



class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by("-created_at")
    serializer_class = BookingSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["customer_name", "customer_email"]

    def get_queryset(self):
        qs = super().get_queryset()
        venue_id = self.request.query_params.get("venue")
        if venue_id:
            qs = qs.filter(venue_id=venue_id)
        return qs

    # Example custom action: cancel booking (POST /api/bookings/{id}/cancel/)
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        booking.status = "cancelled"
        booking.save()
        return Response(
            {"status": "Booking cancelled", "id": booking.id},
            status=status.HTTP_200_OK
        )
    # Custom endpoint: /bookings/findByStatus?status=active
    @action(detail=False, methods=["get"])
    def findByStatus(self, request):
        status_param = request.query_params.get("status", None)
        if status_param:
            bookings = Booking.objects.filter(status=status_param)
        else:
            bookings = Booking.objects.all()
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
    
    # Custom endpoint: /bookings/{id}/uploadDocument
    @action(detail=True, methods=["post"])
    def uploadDocument(self, request, pk=None):
        booking = self.get_object()
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        # In a real app, save file to booking record or storage
        return Response(
            {"status": "File uploaded", "filename": file.name, "booking_id": booking.id},
            status=200
        )
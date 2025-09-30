# bookings/urls.py
from rest_framework import routers
from .views import VenueViewSet, BookingViewSet

router = routers.DefaultRouter()
router.register(r"venues", VenueViewSet, basename="venues")
router.register(r"bookings", BookingViewSet, basename="bookings")

urlpatterns = router.urls

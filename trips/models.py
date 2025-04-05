from django.db import models
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

class Trip(models.Model):
    current_location = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    cycle_used = models.IntegerField()
    current_lat = models.FloatField(null=True, blank=True)
    current_lng = models.FloatField(null=True, blank=True)
    pickup_lat = models.FloatField(null=True, blank=True)
    pickup_lng = models.FloatField(null=True, blank=True)
    dropoff_lat = models.FloatField(null=True, blank=True)
    dropoff_lng = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def geocode_with_retry(self, geolocator, location_str, retries=3, delay=1):
        for attempt in range(retries):
            try:
                return geolocator.geocode(location_str, exactly_one=True, timeout=10)
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                if attempt < retries - 1:
                    time.sleep(delay)
                    continue
                print(f"Geocoding failed for '{location_str}' after {retries} attempts: {e}")
                return None

    def save(self, *args, **kwargs):
        geolocator = Nominatim(user_agent="eld_log")
        locations = {
            "current": self.current_location,
            "pickup": self.pickup_location,
            "dropoff": self.dropoff_location
        }

        for key, value in locations.items():
            if value:
                location = self.geocode_with_retry(geolocator, value)
                if location:
                    setattr(self, f"{key}_lat", location.latitude)
                    setattr(self, f"{key}_lng", location.longitude)
                else:
                    setattr(self, f"{key}_lat", None)
                    setattr(self, f"{key}_lng", None)

        super().save(*args, **kwargs)

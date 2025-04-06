from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Trip
from .serializers import TripSerializer
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import logging

logger = logging.getLogger(__name__)
class LocationSearchView(APIView):
    authentication_classes = []  
    permission_classes = []
    def geocode_with_retry(self, geolocator, query, retries=3, delay=1):
        for attempt in range(retries):
            try:
                return geolocator.geocode(query, exactly_one=False, timeout=10)
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                if attempt < retries - 1:
                    time.sleep(delay)
                    continue
                print(f"Geocoding failed for '{query}' after {retries} attempts: {e}")
                return None

    def get(self, request):
        query = request.GET.get("query", "")
        geolocator = Nominatim(user_agent="eld_log")

        locations = self.geocode_with_retry(geolocator, query)

        results = []
        if locations:
            for loc in locations:
                results.append({
                    "name": loc.address,
                    "lat": loc.latitude,
                    "lng": loc.longitude
                })

        return Response(results)

class TripView(APIView):
    authentication_classes = []  
    permission_classes = []
    def get(self, request, id=None):
        try:
            if id:
                trip = Trip.objects.get(id=id)
                serializer = TripSerializer(trip)
                return Response(serializer.data)
            else:
                trips = Trip.objects.all()
                serializer = TripSerializer(trips, many=True)
                return Response(serializer.data)
        except Exception as e:
            logger.exception("Error in TripView")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            serializer = TripSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Trip created", "trip": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Error in TripView")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    def put(self, request, id):
        try:
            trip = Trip.objects.get(id=id)
            serializer = TripSerializer(trip, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Trip updated", "trip": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Trip.DoesNotExist:
            return Response({"error": "Trip not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            trip = Trip.objects.get(id=id)
            trip.delete()
            return Response({"message": "Trip deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Trip.DoesNotExist:
            return Response({"error": "Trip not found"}, status=status.HTTP_404_NOT_FOUND)

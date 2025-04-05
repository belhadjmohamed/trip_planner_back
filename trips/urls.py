from django.urls import path
from .views import TripView,LocationSearchView

urlpatterns = [
    path('trips/', TripView.as_view(), name='trip'),
    path('trips/<int:id>/', TripView.as_view(), name='trip-detail'),  
    path('locations/', LocationSearchView.as_view(), name='location-search')
]

from rest_framework import serializers
from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = Trip
        fields = '__all__'

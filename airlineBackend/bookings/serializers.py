# Create a DJANGO REST FRAMEWORK serializer for the Flight model
from rest_framework import serializers

from . import models


class FlightSerializer(serializers.ModelSerializer):
    """Serializer for the Flight model."""

    # Represent the target of the foreign key as a string, not an ID
    fromLocation = serializers.StringRelatedField()
    toLocation = serializers.StringRelatedField()

    class Meta:
        model = models.Flight
        fields = "__all__"

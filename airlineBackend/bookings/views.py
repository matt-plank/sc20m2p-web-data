from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers


class FlightView(APIView):
    """Flight view."""

    def get(self, request, format=None):
        """Get all flights."""
        all_flights = models.Flight.objects.all()
        serialized_flights = serializers.FlightSerializer(all_flights, many=True)

        return Response(data=serialized_flights.data, status=status.HTTP_200_OK)

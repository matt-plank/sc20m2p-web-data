import uuid

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


class LocationView(APIView):
    """Location view."""

    def get(self, request, format=None):
        """Get all locations."""
        all_locations = models.Location.objects.all()
        serialized_locations = serializers.LocationSerializer(all_locations, many=True)

        return Response(data=serialized_locations.data, status=status.HTTP_200_OK)


class BookingView(APIView):
    """Booking view."""

    def post(self, request):
        """Create a new booking."""

        # Get the flight ID, user's name, and seat number from request JSON
        flight_id = request.data.get("flight_id")
        name = request.data.get("name")
        seat_number = request.data.get("seat_number")

        # Check there is a flight with id flight_id
        flight = models.Flight.objects.filter(id=flight_id).first()
        if flight is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check the seat is between 1 and the capacity
        if seat_number < 1 or seat_number > flight.capacity:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Check there is no booking with the same flight and seat number
        testBooking = models.Booking.objects.filter(flight=flight, seatNumber=seat_number).first()
        if testBooking is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Create the booking
        booking = models.Booking.objects.create(
            flight=flight,
            userName=name,
            seatNumber=seat_number,
        )

        booking.save()

        # Return the uuid of the booking
        return Response(data={"bookingID": booking.id}, status=status.HTTP_201_CREATED)  # type: ignore

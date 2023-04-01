from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, payments, serializers


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


class PaymentNotificationView(APIView):
    """Payment notification view."""

    def post(self, request):
        """Create a new payment notification."""

        # Get the booking ID and payment provider ID from request JSON
        booking_id = request.data.get("booking_id")
        payment_provider_name = request.data.get("payment_provider")

        # Find the payment provider
        payment_provider = models.PaymentProvider.objects.filter(name=payment_provider_name).first()

        if payment_provider is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Find the booking
        booking = models.Booking.objects.filter(id=booking_id).first()

        if booking is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check payment with the payment provider
        if not payments.check_payment(booking, payment_provider, assume_true=True):
            return Response(data={"message": "Could not verify payment"}, status=status.HTTP_400_BAD_REQUEST)

        # Mark booking as paid
        booking.activated = True
        booking.save()

        return Response(status=status.HTTP_200_OK)

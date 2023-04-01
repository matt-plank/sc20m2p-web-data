from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import db, models, payments, serializers


class FlightView(APIView):
    """Flight view."""

    def get(self, request):
        """Get all flights."""
        all_flights = db.all_flights()
        serialized_flights = serializers.FlightSerializer(all_flights, many=True)

        return Response(data=serialized_flights.data, status=status.HTTP_200_OK)


class LocationView(APIView):
    """Location view."""

    def get(self, request):
        """Get all locations."""
        all_locations = db.all_locations()
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
        flight = db.flight_by_id(flight_id)
        if flight is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check the seat is between 1 and the capacity
        if seat_number < 1 or seat_number > flight.capacity:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Check there is no booking with the same flight and seat number
        testBooking = db.booking_by_flight_and_seat_number(flight, seat_number)
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
        payment_provider = db.payment_provider_from_name(payment_provider_name)

        if payment_provider is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Find the booking
        booking = db.booking_by_id(booking_id)

        if booking is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check payment with the payment provider
        if not payments.check_payment(booking, payment_provider, assume_true=True):
            return Response(data={"message": "Could not verify payment"}, status=status.HTTP_400_BAD_REQUEST)

        # Mark booking as paid
        booking.activated = True
        booking.save()

        return Response(data={"bookingID": booking.id}, status=status.HTTP_200_OK)  # type: ignore

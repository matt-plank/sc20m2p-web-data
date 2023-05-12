import uuid

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import db, models, payments, serializers


class FlightView(APIView):
    """Flight view.

    Returns lists of flights according to various parameters."""

    def get(self, request):
        """Get a list of flights."""
        from_location = request.query_params.get("fromLocation")
        to_location = request.query_params.get("toLocation")
        date = request.query_params.get("date")

        all_flights = db.all_flights(
            from_location=db.location_by_name(from_location),
            to_location=db.location_by_name(to_location),
            date=date,
        )

        serialized_flights = serializers.FlightSerializer(all_flights, many=True).data

        for flight in serialized_flights:
            flight["flightID"] = flight["id"]
            del flight["id"]

        return Response(data=serialized_flights, status=status.HTTP_200_OK)


class BookingView(APIView):
    """Booking view.

    This view is called when the client wants to reserve a seat for a flight while they make a payment.
    The booking is created, but not activated.
    The main purpose of this view is to provide the client with a booking ID, which they can use to make
    a payment with their chosen payment service. Then the airline can verify the payment is made only for this booking."""

    def post(self, request):
        """Create a new booking."""

        # Get the flight ID, user's name, and seat number from request JSON
        flight_id = request.data.get("flightID")
        name = request.data.get("firstName") + " " + request.data.get("lastName")

        # Check there is a flight with id flight_id
        flight = db.flight_by_id(flight_id)
        if flight is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check if there are seats available
        if flight.capacity < 1:
            return Response(status=status.HTTP_410_GONE)

        # Create the booking
        booking = models.Booking.objects.create(
            flight=flight,
            userName=name,
        )

        booking.save()

        # Return the uuid of the booking
        return Response(
            {
                "bookingID": str(booking.id),
                "accountNo": "87654321",
                "sortCode": "112233",
                "cost": str(flight.ticketPrice),
            },
            status=status.HTTP_201_CREATED,
            content_type="application/json",
        )


class PaymentNotificationView(APIView):
    """Payment notification view.

    This view is called when the client wants to let the airline know that they've paid
    for a booking. The airline can then verify this payment, and send a booking confirmation
    to the client."""

    def post(self, request):
        """Create a new payment notification."""

        # Get the booking ID and payment provider ID from request JSON
        booking_id = request.data.get("bookingID")
        payment_provider_name = request.data.get("paymentProvider")

        # Find the payment provider

        if payment_provider_name is None:
            return Response(data={"message": "Please indicate payment provider"}, status=status.HTTP_400_BAD_REQUEST)

        payment_provider = db.payment_provider_from_name(payment_provider_name)

        if payment_provider is None:
            return Response(data={"message": "No such payment provider"}, status=status.HTTP_400_BAD_REQUEST)

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

        # Reduce flight capacity
        booking.flight.capacity -= 1
        booking.flight.save()

        return Response({"bookingID": booking.id}, status=status.HTTP_200_OK, content_type="application/json")  # type: ignore

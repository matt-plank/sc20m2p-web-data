"""Tess the entire process of finding a flight, creating a booking, and activating it from the user perspective."""

from bookings import models
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class TestIntegration(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Add locations to the test database for Prague and Leeds
        models.Location.objects.create(name="Prague")
        models.Location.objects.create(name="Leeds")

        models.Flight.objects.create(
            toLocation=models.Location.objects.get(name="Prague"),
            fromLocation=models.Location.objects.get(name="Leeds"),
            date="2023-06-01",
            capacity=100,
            ticketPrice=23.0,
        )

        models.Flight.objects.create(
            toLocation=models.Location.objects.get(name="Leeds"),
            fromLocation=models.Location.objects.get(name="Prague"),
            date="2023-06-02",
            capacity=100,
            ticketPrice=19.0,
        )

        models.PaymentProvider.objects.create(name="PayPal", url="https://paypalAPI.com/")

    def test_find_create_activate_booking(self):
        """Test finding a flight, creating a booking, and activating it."""
        # Find a suitable flight
        flights = self.client.get("/bookings/flights", {"from": "Leeds", "to": "Prague", "date": "2023-06-01"})

        self.assertEqual(flights.status_code, status.HTTP_200_OK)

        # Create a booking for that flight
        booking_response = self.client.post(
            "/bookings/booking",
            {
                "flightID": flights.json()[0]["id"],
                "firstName": "John",
                "lastName": "Smith",
            },
        )

        self.assertEqual(booking_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(booking_response.json(), {"bookingID": booking_response.json()["bookingID"]})

        # Activate the booking for that flight (by notification of payment)
        response = self.client.post(
            "/bookings/paymentNotification",
            {
                "bookingID": booking_response.json()["bookingID"],
                "paymentProvider": "PayPal",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"bookingID": response.json()["bookingID"]})

import uuid

from bookings import models
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class TestBookings(TestCase):
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

    def test_create_booking_successful(self):
        """Test creating a booking (unpaid)."""
        response = self.client.post(
            "/bookings/booking",
            {
                "flightID": 1,
                "firstName": "John",
                "lastName": "Smith",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"bookingID": response.json()["bookingID"]})

    def test_create_booking_bad_flight_id(self):
        """Test creating a booking with a bad flight id."""
        response = self.client.post(
            "/bookings/booking",
            {
                "flightID": 3,
                "firstName": "John",
                "lastName": "Smith",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_then_activate_booking(self):
        """Test creating a booking and then activating it."""
        response = self.client.post(
            "/bookings/booking",
            {
                "flightID": 1,
                "firstName": "John",
                "lastName": "Smith",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"bookingID": response.json()["bookingID"]})

        response = self.client.post(
            "/bookings/paymentNotification",
            {
                "bookingID": response.json()["bookingID"],
                "paymentProvider": "PayPal",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"bookingID": response.json()["bookingID"]})

    def test_create_then_activate_booking_bad_booking_id(self):
        """Test creating a booking and then activating it with a bad booking id."""
        response = self.client.post(
            "/bookings/booking",
            {
                "flightID": 1,
                "firstName": "John",
                "lastName": "Smith",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"bookingID": response.json()["bookingID"]})

        response = self.client.post(
            "/bookings/paymentNotification",
            {
                "bookingID": uuid.uuid4(),
                "paymentProvider": "PayPal",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_then_activate_booking_bad_payment_provider(self):
        """Test creating a booking and then activating it with a bad payment provider."""
        response = self.client.post(
            "/bookings/booking",
            {
                "flightID": 1,
                "firstName": "John",
                "lastName": "Smith",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"bookingID": response.json()["bookingID"]})

        response = self.client.post(
            "/bookings/paymentNotification",
            {
                "bookingID": response.json()["bookingID"],
                "paymentProvider": "Stripe",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

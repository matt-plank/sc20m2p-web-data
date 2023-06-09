from bookings import models
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class FlightViewTestCase(TestCase):
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

    def test_get_all_flights(self):
        """Test getting all flights."""
        response = self.client.get("/bookings/flights")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [
                {
                    "flightID": 1,
                    "toLocation": "Prague",
                    "fromLocation": "Leeds",
                    "date": "2023-06-01",
                    "capacity": 100,
                    "ticketPrice": 23.0,
                },
                {
                    "flightID": 2,
                    "toLocation": "Leeds",
                    "fromLocation": "Prague",
                    "date": "2023-06-02",
                    "capacity": 100,
                    "ticketPrice": 19.0,
                },
            ],
        )

    def test_get_flights_from_leeds_to_prague(self):
        """Test getting flights from Leeds to Prague."""
        response = self.client.get("/bookings/flights?fromLocation=Leeds&toLocation=Prague")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [
                {
                    "flightID": 1,
                    "toLocation": "Prague",
                    "fromLocation": "Leeds",
                    "date": "2023-06-01",
                    "capacity": 100,
                    "ticketPrice": 23.0,
                },
            ],
        )

    def test_get_flights_from_leeds_to_prague_on_2023_06_05(self):
        """Test getting flights from Leeds to Prague on 2023-06-05."""
        response = self.client.get("/bookings/flights?fromLocation=Leeds&toLocation=Prague&date=2023-06-05")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

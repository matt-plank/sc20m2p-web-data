"""Use the unittest harness to run integration tests on the online airline backend"""

import unittest

import requests

FLIGHT_URL: str = "http://sc20m2p.pythonanywhere.com/bookings/flights"
BOOKING_URL: str = "http://sc20m2p.pythonanywhere.com/bookings/booking"
PAYMENT_URL: str = "http://sc20m2p.pythonanywhere.com/bookings/paymentNotification"


class TestIntegration(unittest.TestCase):
    def test_find_create_activate_booking(self):
        """Test finding a flight, creating a booking, and activating it."""
        # Find a suitable flight
        flights = requests.get(
            FLIGHT_URL,
            {
                "from": "MAN",
                "to": "PRG",
                "date": "2023-06-01",
            },
        )

        # Create a booking for that flight
        booking_response = requests.post(
            BOOKING_URL,
            {
                "flightID": flights.json()[0]["flightID"],
                "firstName": "John",
                "lastName": "Smith",
            },
        )

        # Activate the booking for that flight (by notification of payment)
        response = requests.post(
            PAYMENT_URL,
            {
                "bookingID": booking_response.json()["bookingID"],
                "paymentProvider": "PayPal",
            },
        )

        print(response.json())

        assert response.status_code == 200
        assert response.json() == {"bookingID": response.json()["bookingID"]}

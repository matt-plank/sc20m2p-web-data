import requests
from django.conf import settings

from . import models


def check_payment(booking: models.Booking, cost: float, payment_provider: models.PaymentProvider) -> bool:
    """Check payment for a booking."""
    if settings.TESTING:  # Do not check payment in testing mode
        return True

    response = requests.get(payment_provider.url, {"bookingID": str(booking.id), "cost": cost})

    if response.status_code != 200:
        return False

    response_json = response.json()

    if response_json["amount"] != booking.flight.ticketPrice:
        return False

    return True

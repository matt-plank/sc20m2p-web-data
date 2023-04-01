import requests

from . import models


def check_payment(booking: models.Booking, payment_provider: models.PaymentProvider, assume_true: bool = False) -> bool:
    """Check payment for a booking."""
    if assume_true:
        return True

    response = requests.post(payment_provider.url, data={"booking_id": booking.id})  # type: ignore

    if response.status_code != 200:
        return False

    response_json = response.json()

    if response_json["amount"] != booking.flight.ticketPrice:
        return False

    return True

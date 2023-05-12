import uuid

from django.db import models


class Location(models.Model):
    """A location where a flight can depart from or arrive at."""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Flight(models.Model):
    """A flight from one location to another on a specific date."""

    fromLocation = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="fromLocation")
    toLocation = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="toLocation")
    date = models.DateField()
    capacity = models.IntegerField()
    ticketPrice = models.FloatField()

    def __str__(self):
        return f"{self.fromLocation} to {self.toLocation} on {self.date}"


class Booking(models.Model):
    """A booking for a specific flight."""

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    userName = models.CharField(max_length=255)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.userName} booked on {self.flight}"


class PaymentProvider(models.Model):
    """A payment provider.

    Used to track which payment providers the airline will accept payments with.
    The url field is the URL of the payment provider's API, used to verify payments.
    A payment provider database record can only be created / managed on the admin dashboard."""

    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

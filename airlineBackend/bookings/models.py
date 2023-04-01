from django.contrib.auth.models import User
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

    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    userName = models.CharField(max_length=255)
    seatNumber = models.IntegerField()
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.userName} booked seat {self.seatNumber} on {self.flight}"


class PaymentProvider(models.Model):
    """A payment provider."""

    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

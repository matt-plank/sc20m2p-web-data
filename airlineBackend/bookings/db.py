"""Database access functions.

This module contains functions that access the database. I would consider
it to be good practice to put all database access in one place, so that
if you ever need to change the database, you only need to change this
module."""

from . import models


def payment_provider_from_name(name: str) -> models.PaymentProvider | None:
    """Get a payment provider from its name."""
    return models.PaymentProvider.objects.filter(name=name).first()


def booking_by_id(id: int) -> models.Booking | None:
    """Get a booking by its ID."""
    return models.Booking.objects.filter(id=id).first()


def flight_by_id(id: int) -> models.Flight | None:
    """Get a flight by its ID."""
    return models.Flight.objects.filter(id=id).first()


def booking_by_flight_and_seat_number(flight: models.Flight, seat_number: int) -> models.Booking | None:
    """Get a booking by its flight and seat number."""
    return models.Booking.objects.filter(flight=flight, seatNumber=seat_number).first()


def all_locations():
    """Get all locations."""
    return models.Location.objects.all()


def location_by_name(name: str) -> models.Location | None:
    """Get a location by its name."""
    return models.Location.objects.filter(name=name).first()


def all_flights(from_location: models.Location | None = None, to_location: models.Location | None = None, date: str | None = None):
    """Get all flights."""
    flights = models.Flight.objects

    if from_location is not None:
        flights = flights.filter(fromLocation=from_location)

    if to_location is not None:
        flights = flights.filter(toLocation=to_location)

    if date is not None:
        flights = flights.filter(date=date)

    return flights.all()

# URLs to point to the views in the bookings app
from django.urls import path

from . import views

urlpatterns = [
    path("flights", views.FlightView.as_view()),
]

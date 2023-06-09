# URLs to point to the views in the bookings app
from django.urls import path

from . import views

urlpatterns = [
    path("flights", views.FlightView.as_view()),
    path("booking", views.BookingView.as_view()),
    path("paymentNotification", views.PaymentNotificationView.as_view()),
]

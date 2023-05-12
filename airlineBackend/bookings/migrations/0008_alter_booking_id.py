# Generated by Django 4.1.7 on 2023-05-12 16:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("bookings", "0007_remove_booking_seatnumber"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]

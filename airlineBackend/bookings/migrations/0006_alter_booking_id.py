# Generated by Django 4.1.7 on 2023-05-12 14:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookings", "0005_paymentprovider"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="id",
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
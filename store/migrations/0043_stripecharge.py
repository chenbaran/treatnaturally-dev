# Generated by Django 4.2.5 on 2023-09-14 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("store", "0042_order_stripe_charge_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="StripeCharge",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stripe_charge_id", models.CharField(max_length=50)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("paid", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 4.1.6 on 2023-03-16 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_remove_optionalshippingaddress_order_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='optionalshippingaddress',
            name='order_notes',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]

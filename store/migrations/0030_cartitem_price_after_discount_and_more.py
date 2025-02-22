# Generated by Django 4.1.6 on 2023-03-20 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0029_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='price_after_discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='price_after_discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]

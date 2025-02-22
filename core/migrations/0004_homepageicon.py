# Generated by Django 4.1.6 on 2023-06-13 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_graphics_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomePageIcon",
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
                ("title", models.CharField(blank=True, max_length=255, null=True)),
                ("subtitle", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="graphics/home_page_slider/"
                    ),
                ),
                (
                    "graphics",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="home_page_icon",
                        to="core.graphics",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Home Page Icons",
                "ordering": ["id"],
            },
        ),
    ]

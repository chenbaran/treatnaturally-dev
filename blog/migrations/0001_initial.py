# Generated by Django 4.1.5 on 2023-01-22 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True, null=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('tag', models.ManyToManyField(blank=True, to='tags.tag')),
            ],
        ),
    ]

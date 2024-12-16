# Generated by Django 5.1.4 on 2024-12-15 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_booking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='movieslot',
            name='unique_slot_time_per_screen',
        ),
        migrations.AddField(
            model_name='movieslot',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]

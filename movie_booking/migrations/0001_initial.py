# Generated by Django 5.1.4 on 2024-12-15 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('duration', models.IntegerField(help_text='Movie duration in minutes')),
            ],
        ),
        migrations.CreateModel(
            name='Screen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('seat_capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Theatre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUnavailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('is_fully_unavailable', models.BooleanField(default=False)),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_unavailabilities', to='movie_booking.screen')),
            ],
        ),
        migrations.AddField(
            model_name='screen',
            name='theatre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screens', to='movie_booking.theatre'),
        ),
        migrations.CreateModel(
            name='MovieSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie_booking.movie')),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_slots', to='movie_booking.screen')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('screen', 'start_time', 'end_time'), name='unique_slot_time_per_screen')],
            },
        ),
        migrations.CreateModel(
            name='WeeklySchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10)),
                ('open_time', models.TimeField()),
                ('close_time', models.TimeField()),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weekly_schedules', to='movie_booking.screen')),
            ],
            options={
                'unique_together': {('screen', 'day_of_week')},
            },
        ),
        migrations.CreateModel(
            name='WeeklyUnavailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weekly_unavailabilities', to='movie_booking.screen')),
            ],
            options={
                'unique_together': {('screen', 'day_of_week', 'start_time', 'end_time')},
            },
        ),
    ]

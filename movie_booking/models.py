from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Theatre(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Screen(models.Model):
    theatre = models.ForeignKey(Theatre, related_name='screens', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    seat_capacity = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('theatre', 'name')

    def __str__(self):
        return f"{self.theatre.name} - {self.name}"

class Movie(models.Model):
    title = models.CharField(max_length=200)
    duration = models.IntegerField(help_text="Movie duration in minutes")

    def __str__(self):
        return self.title

class WeeklySchedule(models.Model):
    screen = models.ForeignKey(Screen, related_name='weekly_schedules', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), 
        ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), 
        ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')
    ])
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        unique_together = ('screen', 'day_of_week')

class WeeklyUnavailability(models.Model):
    screen = models.ForeignKey(Screen, related_name='weekly_unavailabilities', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('screen', 'day_of_week', 'start_time', 'end_time')

class CustomUnavailability(models.Model):
    screen = models.ForeignKey(Screen, related_name='custom_unavailabilities', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_fully_unavailable = models.BooleanField(default=False)

class MovieSlot(models.Model):
    screen = models.ForeignKey(Screen, related_name='movie_slots', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Validate slot doesn't conflict with unavailability
        self.full_clean()
        super().save(*args, **kwargs)
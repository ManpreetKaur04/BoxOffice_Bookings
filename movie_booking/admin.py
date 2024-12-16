# movie_booking/admin.py
from django.contrib import admin
from .models import Theatre, Screen, Movie, WeeklySchedule, WeeklyUnavailability, CustomUnavailability, MovieSlot

@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ('name', 'theatre', 'seat_capacity')
    list_filter = ('theatre',)
    search_fields = ('name', 'theatre__name')

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration')
    search_fields = ('title',)

@admin.register(WeeklySchedule)
class WeeklyScheduleAdmin(admin.ModelAdmin):
    list_display = ('screen', 'day_of_week', 'open_time', 'close_time')
    list_filter = ('screen', 'day_of_week')

@admin.register(WeeklyUnavailability)
class WeeklyUnavailabilityAdmin(admin.ModelAdmin):
    list_display = ('screen', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('screen', 'day_of_week')

@admin.register(CustomUnavailability)
class CustomUnavailabilityAdmin(admin.ModelAdmin):
    list_display = ('screen', 'date', 'start_time', 'end_time', 'is_fully_unavailable')
    list_filter = ('screen', 'date', 'is_fully_unavailable')

@admin.register(MovieSlot)
class MovieSlotAdmin(admin.ModelAdmin):
    list_display = ('screen', 'movie', 'start_time', 'end_time')
    list_filter = ('screen', 'movie')
    search_fields = ('movie__title',)
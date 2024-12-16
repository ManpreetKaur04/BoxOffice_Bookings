from datetime import datetime, timedelta
from django.db.models import Q
from django.utils import timezone
from .models import *

def generate_movie_slots(screen, start_date, end_date):
    """
    Dynamically generate movie slots for a screen within a date range
    considering weekly schedules and unavailabilities.
    
    Args:
        screen (Screen): The screen to generate slots for.
        start_date (date): Start of the slot generation range.
        end_date (date): End of the slot generation range.
    
    Returns:
        list: Generated movie slots.
    """
    # Fetch relevant configurations
    weekly_schedules = WeeklySchedule.objects.filter(screen=screen)
    weekly_unavailabilities = WeeklyUnavailability.objects.filter(screen=screen)
    custom_unavailabilities = CustomUnavailability.objects.filter(screen=screen)
    
    # Fetch available movies
    available_movies = Movie.objects.all()
    
    # Generated slots to be returned
    slots = []
    
    # Iterate through each day in the date range
    current_date = start_date
    while current_date <= end_date:
        # Check if the entire date is unavailable
        if custom_unavailabilities.filter(
            date=current_date, 
            is_fully_unavailable=True
        ).exists():
            current_date += timedelta(days=1)
            continue
        
        # Find weekly schedule for this day
        day_schedule = weekly_schedules.filter(
            day_of_week=current_date.strftime('%A')
        ).first()
        
        if not day_schedule:
            current_date += timedelta(days=1)
            continue
        
        # Convert schedule times to datetime
        day_open = timezone.make_aware(datetime.combine(current_date, day_schedule.open_time))
        day_close = timezone.make_aware(datetime.combine(current_date, day_schedule.close_time))
        
        # Find daily unavailability slots
        daily_unavailabilities = list(weekly_unavailabilities.filter(
            day_of_week=current_date.strftime('%A')
        )) + list(custom_unavailabilities.filter(
            date=current_date,
            start_time__isnull=False,
            end_time__isnull=False
        ))

        # Sort movies by duration (shorter movies first for better slot packing)
        sorted_movies = sorted(available_movies, key=lambda m: m.duration)
        
        # Current slot start time
        current_slot_start = day_open
        
        for movie in sorted_movies:
            # Calculate slot end time
            slot_duration = timedelta(minutes=movie.duration)
            current_slot_end = current_slot_start + slot_duration
            
            # Check if slot fits within theatre hours
            if current_slot_end > day_close:
                break
            
            # Check if slot conflicts with weekly unavailabilities
            conflicting_weekly_unavailabilities = weekly_unavailabilities.filter(
                Q(start_time__lt=current_slot_end.time(), end_time__gt=current_slot_start.time()) |
                Q(start_time__lt=current_slot_start.time(), end_time__gt=current_slot_end.time())
            )

            # Check if slot conflicts with custom unavailabilities
            conflicting_custom_unavailabilities = custom_unavailabilities.filter(
                Q(start_time__lt=current_slot_end.time(), end_time__gt=current_slot_start.time()) |
                Q(start_time__lt=current_slot_start.time(), end_time__gt=current_slot_end.time())
            )

            # If no conflicts in both weekly and custom unavailabilities
            if not conflicting_weekly_unavailabilities.exists() and not conflicting_custom_unavailabilities.exists():
                # Create movie slot
                movie_slot = MovieSlot(
                    screen=screen,
                    movie=movie,
                    start_time=current_slot_start,
                    end_time=current_slot_end,
                    is_available=True
                )
                
                # Attempt to save (this will trigger model validation)
                try:
                    movie_slot.full_clean()
                    movie_slot.save()
                    slots.append(movie_slot)
                except Exception as e:
                    # Log any validation errors (consider using logging instead of print)
                    print(f"Could not create slot for {movie.title} at {current_slot_start}: {e}")
            
            # Move to next potential slot
            current_slot_start = current_slot_end
        
        current_date += timedelta(days=1)
    
    return slots

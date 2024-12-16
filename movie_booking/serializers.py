
from rest_framework import serializers
from .models import Theatre, Screen, WeeklySchedule, WeeklyUnavailability, CustomUnavailability, MovieSlot, Movie

class WeeklyScheduleSerializer(serializers.Serializer):
    open = serializers.TimeField(format="%H:%M")
    close = serializers.TimeField(format="%H:%M")


class WeeklyUnavailabilitySerializer(serializers.Serializer):
    start = serializers.TimeField(format="%H:%M")
    end = serializers.TimeField(format="%H:%M")

class AvailabilityConfigSerializer(serializers.Serializer):
    weekly_schedule = serializers.DictField(
        child=WeeklyScheduleSerializer()
    )
    weekly_unavailability = serializers.DictField(
        child=serializers.ListField(
            child=WeeklyUnavailabilitySerializer(),
            required=False
        ),
        required=False
    )

    def validate_weekly_schedule(self, value):
        # Validate the weekly schedule times
        for day, schedule in value.items():
            if schedule['open'] >= schedule['close']:
                raise serializers.ValidationError(f"Open time must be before close time for {day}.")
        return value

    def validate_weekly_unavailability(self, value):
        # Validate unavailability time intervals
        for day, intervals in value.items():
            for interval in intervals:
                if interval['start'] >= interval['end']:
                    raise serializers.ValidationError(
                        f"Unavailability start time must be before end time for {day}."
                    )
        return value




class CustomUnavailabilitySerializer(serializers.Serializer):
    screen_name = serializers.CharField()
    unavailable_slots = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        ),
        required=False
    )
    unavailable_dates = serializers.ListField(
        child=serializers.DateField(),
        required=False
    )

    def validate(self, data):
        if not data.get('unavailable_slots') and not data.get('unavailable_dates'):
            raise serializers.ValidationError("Either 'unavailable_slots' or 'unavailable_dates' must be provided.")
        return data


class MovieSlotSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = MovieSlot
        fields = ['id', 'screen_id', 'movie_title', 'start_time', 'end_time', 'is_available']


class TheatreSerializer(serializers.ModelSerializer):
    screens = serializers.SerializerMethodField()

    class Meta:
        model = Theatre
        fields = ['id', 'name', 'screens', 'location']

    def get_screens(self, obj):
        # Fetch screens related to the specific theatre
        screens = obj.screens.all()  # Using the reverse relationship via related_name
        # Return the screens as a list of dictionaries
        return [{'id': screen.id, 'name': screen.name, 'seat_capacity': screen.seat_capacity} for screen in screens]


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = '__all__'

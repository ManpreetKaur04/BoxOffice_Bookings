from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Screen, WeeklySchedule, WeeklyUnavailability, CustomUnavailability, Theatre
from .serializers import AvailabilityConfigSerializer, CustomUnavailabilitySerializer, MovieSlotSerializer, TheatreSerializer, ScreenSerializer
from .services import generate_movie_slots
from datetime import datetime

class TheatreAvailabilityView(APIView):
    def post(self, request, theatre_id):
        serializer = AvailabilityConfigSerializer(data=request.data)
        if serializer.is_valid():
            screens = Screen.objects.filter(theatre_id=theatre_id)
            
            # Process weekly schedules
            weekly_schedule_data = serializer.validated_data['weekly_schedule']
            for day, schedule in weekly_schedule_data.items():
                weekly_schedules = [
                    WeeklySchedule(
                        screen=screen,
                        day_of_week=day,
                        open_time=schedule['open'],
                        close_time=schedule['close']
                    ) for screen in screens
                ]
                WeeklySchedule.objects.bulk_create(weekly_schedules)

            # Process weekly unavailabilities
            weekly_unavailability_data = serializer.validated_data.get('weekly_unavailability', {})
            for day, unavailabilities in weekly_unavailability_data.items():
                weekly_unavailabilities = [
                    WeeklyUnavailability(
                        screen=screen,
                        day_of_week=day,
                        start_time=unavail['start'],
                        end_time=unavail['end']
                    ) for screen in screens for unavail in unavailabilities
                ]
                WeeklyUnavailability.objects.bulk_create(weekly_unavailabilities)

            return Response({'message': 'Availability configured successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUnavailabilityView(APIView):
    def post(self, request, theatre_id):
        serializer = CustomUnavailabilitySerializer(data=request.data)
        if serializer.is_valid():
            # Ensure screen exists for the given theatre
            screen = get_object_or_404(Screen, name=serializer.validated_data['screen_name'], theatre_id=theatre_id)

            # Process unavailable slots
            custom_unavailabilities = []
            if 'unavailable_slots' in serializer.validated_data:
                for slot in serializer.validated_data['unavailable_slots']:
                    custom_unavailabilities.append(
                        CustomUnavailability(
                            screen=screen,
                            date=slot['date'],
                            start_time=slot['start'],
                            end_time=slot['end']
                        )
                    )

            # Process fully unavailable dates
            if 'unavailable_dates' in serializer.validated_data:
                for date in serializer.validated_data['unavailable_dates']:
                    custom_unavailabilities.append(
                        CustomUnavailability(
                            screen=screen,
                            date=date,
                            is_fully_unavailable=True
                        )
                    )

            CustomUnavailability.objects.bulk_create(custom_unavailabilities)

            return Response({'message': 'Custom unavailability configured successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieSlotsView(APIView):
    def get(self, request, theatre_id):
        screen_id = request.query_params.get('screen_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not all([screen_id, start_date, end_date]):
            return Response(
                {'error': 'screen_id, start_date, and end_date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Handle case where screen_id is invalid
        try:
            screen = Screen.objects.get(id=screen_id)
        except Screen.DoesNotExist:
            return Response(
                {'error': 'Screen not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate date formats
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format, should be YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate movie slots
        slots = generate_movie_slots(screen, start_date, end_date)

        # Serialize and return slots
        serializer = MovieSlotSerializer(slots, many=True)
        return Response(serializer.data)


class TheatreCreateView(generics.CreateAPIView):
    """
    Endpoint to create a new theatre
    """
    serializer_class = TheatreSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        theatre = serializer.save()
        
        # Optional: Create screens if provided in the request
        screens_data = request.data.get('screens', [])
        screens = []
        for screen_data in screens_data:
            screen_serializer = ScreenSerializer(data={
                'theatre': theatre.id,
                'screen': screen_data.get('screen')
            })
            if screen_serializer.is_valid():
                screen = screen_serializer.save()
                screens.append(screen)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ScreenCreateView(generics.CreateAPIView):
    """
    Endpoint to create a new screen for a specific theatre
    """
    serializer_class = ScreenSerializer

    def create(self, request, theatre_id, *args, **kwargs):
        # Validate theatre exists
        try:
            theatre = Theatre.objects.get(id=theatre_id)
        except Theatre.DoesNotExist:
            return Response(
                {'error': 'Theatre not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Prepare screen data
        screen_data = request.data.copy()
        screen_data['theatre'] = theatre.id  

        serializer = self.get_serializer(data=screen_data)
        serializer.is_valid(raise_exception=True)
        screen = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TheatreListView(generics.ListAPIView):
    """
    Endpoint to list all theatres with their screens
    """
    queryset = Theatre.objects.all()
    serializer_class = TheatreSerializer


class TheatreDetailView(generics.RetrieveAPIView):
    """
    Endpoint to retrieve details of a specific theatre
    """
    queryset = Theatre.objects.all()
    serializer_class = TheatreSerializer

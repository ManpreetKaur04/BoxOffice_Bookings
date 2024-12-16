from django.urls import path
from .views import (
    TheatreAvailabilityView, 
    CustomUnavailabilityView, 
    MovieSlotsView, TheatreCreateView, TheatreDetailView, TheatreListView,ScreenCreateView
)

urlpatterns = [
    path('theatre/create/', 
         TheatreCreateView.as_view(), 
         name='theatre-create'),
         
    path('theatre/<int:theatre_id>/screens/create/', 
         ScreenCreateView.as_view(), 
         name='screen-create'),

    path('theatre/', 
         TheatreListView.as_view(), 
         name='theatre-list'),

    path('theatre/<int:pk>/', 
         TheatreDetailView.as_view(), 
         name='theatre-detail'),

    path('theatre/<int:theatre_id>/availability/', 
         TheatreAvailabilityView.as_view(), 
         name='theatre-availability'),

    path('theatre/<int:theatre_id>/custom-unavailability/', 
         CustomUnavailabilityView.as_view(), 
         name='custom-unavailability'),

    path('theatre/<int:theatre_id>/slots/', 
         MovieSlotsView.as_view(), 
         name='movie-slots'),
]
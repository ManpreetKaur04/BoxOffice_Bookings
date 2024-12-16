 README.md
# Movie Booking Backend

Develop a Django-based backend system that dynamically generates and manages movie booking slots for theaters. This focuses on dynamic slot creation, handling complex availability configurations, and providing a query endpoint for users.


### Installation
1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt 
4. Run Migrations:
 ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
```
5. Create a superuser for the Django admin interface:
```bash
python manage.py createsuperuser
```

6. Running the Project:
```bash
python manage.py runserver
```


### Postman Testing Instructions:

Postman Installed: Ensure you have Postman installed on your computer.

API Running: Make sure your Django server is running (e.g., python manage.py runserver).

### Summary of Endpoints

- <ins>Create a Theatre</ins>

   Endpoint: POST /theatre/create/
   
   View: TheatreCreateView
   
   Description: Allows creating a new theater with basic details.
   

- <ins>Create a Screen for a Theatre</ins>
  
   Endpoint: POST /theatre/<int:theatre_id>/screens/create/
   
   View: ScreenCreateView
   
   Description: Adds a new screen to a specified theater.


- <ins>List Theatres</ins>

   Endpoint: GET /theatre/
   
   View: TheatreListView
   
   Description: Fetches a list of all theaters. 
   

- <ins>Theatre Details</ins>
    
   Endpoint: GET /theatre/<int:pk>/
   
   View: TheatreDetailView
   
   Description: Retrieves details of a specific theater by its ID.
 

- <ins>Configure Weekly Availability</ins>
    
   Endpoint: POST /theatre/<int:theatre_id>/availability/
   
   View: TheatreAvailabilityView
   
   Description: Allows configuring weekly opening and unavailability times for a theater.
 

- <ins>Set Custom Unavailability</ins>

   Endpoint: POST /theatre/<int:theatre_id>/custom-unavailability/
   
   View: CustomUnavailabilityView
   
   Description: Sets custom unavailability for specific slots or dates.
   

- <ins>Fetch Available Movie Slots</ins>
  
     Endpoint: GET /theatre/<int:theatre_id>/slots/
     
     View: MovieSlotsView
     
     Description: Retrieves all available slots for a specific theater and screen within a given date range.
     

 ### DEMO RECORDING
 
 [Demo click to watch the video](https://drive.google.com/file/d/192bbj-toKe_W4LrNVSTe41k9WJWgJAwT/view?usp=sharing)
 
### POSTMAN API Documentation

[Postman Documentation](https://documenter.getpostman.com/view/37734920/2sAYHzG34P).

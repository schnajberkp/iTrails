from django.urls import path
from . import views

urlpatterns = [
    path("", views.trail_list, name="trail_list"), # List of all trails
    path("trail/<int:pk>/", views.trail_detail, name="trail_detail"), # Detail view of a single trail
    path("trail/<int:pk>/review/add", views.review_create, name="review_create"), # Create a new review for a trail
    path("trips/", views.my_trips, name="my_trips"), # List of trips for the logged-in user
    path("trips/add/", views.trip_create, name="trip_create"), # Create a new trip for the logged-in user


    # JSON API 
    path("api/trails/", views.trail_list_api, name="trail_list_api"), # List of trails in JSON format
    path("api/trail/<int:pk>/", views.trail_detail_api, name="trail_detail_api"), # Detail view of a single trail in JSON format
    path("api/my_trips/", views.my_trips_api, name="my_trips_api"), # List of trips for the logged-in user in JSON format
    path("api/trail/<int:pk>/reviews/", views.review_create_api, name="review_create_api"), # Create a new review for a trail in JSON format
]
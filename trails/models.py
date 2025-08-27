from django.db import models
from django.conf import settings

# class = table in database
# attributes = columns in table

# Place where trails are located
class Location(models.Model):
    name = models.CharField(max_length=120, unique=True)
    country = models.CharField(max_length=60, default='Czech Republic')
    region = models.CharField(max_length=120, blank=True)

    # Returns readable name for the location
    def __str__(self) -> str:
        return self.name
    
# Tag for categorizing trails
class Tag(models.Model):
    name = models.CharField(max_length=60, unique=True)
    
    def __str__(self) -> str:
        return self.name
    
# Trail model representing a hiking trail
# Each trail has a title, location, length, elevation gain, difficulty, and tags
# It also has a created_at timestamp for when it was added
class Trail(models.Model):
    DIFFICULTY_CHOICES = [
        # Caps for database and logic, lowercase for users in GUI
        ('EASY', 'Easy'),
        ('MODERATE', 'Moderate'),
        ('HARD', 'Hard'),
    ]
    title = models.CharField(max_length=150)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='trails') # PROTECT prevents deletion if trails exist
    length_km = models.DecimalField(max_digits=5, decimal_places=2)
    elevation_gain_m = models.PositiveIntegerField(default=0)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="MODERATE") 
    tags = models.ManyToManyField(Tag, blank=True, related_name="trails") # Many-to-many relationship with Tag
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title 
    
# Review model for user reviews of trails
class Review(models.Model):
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE, related_name="reviews") # If trail is deleted, delete reviews
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="trail_reviews") #If user is deleted, set to NULL, but keep reviews
    rating = models.PositiveSmallIntegerField(default=5) 
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Ensure a user can only leave one review per trail
    class Meta:
        unique_together = ("trail", "user")
        
    def __str__(self) -> str:
        return f"{self.trail} - {self.user} ({self.rating}/5)" # Review representation 
    
# Trip model for user trips to trails
# Each trip has a user, trail, date, and optional note
class Trip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trips") # If user is deleted, delete trips
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE, related_name="trips") # If trail is deleted, delete trips
    date = models.DateField()
    note = models.CharField(max_length=200, blank=True)

    # Ensure trips are ordered by date descending
    class Meta:
        ordering = ["-date"]
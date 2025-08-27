from django.contrib import admin
#Import models from trails app
from .models import Location, Tag, Trail, Review, Trip


# This allows managing these models directly from the Django admin interface
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "region")
    search_fields = ("name", "region")


# This allows managing tags directly from the admin interface
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)

# This allows adding reviews directly from the Trail admin page
class ReviewInline(admin.TabularInline):
    model = Review
    # How many extra empty lines to show for adding new reviews
    extra = 0

# This allows managing trails directly from the admin interface
@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):

    list_display = ("title", "location", "length_km", "elevation_gain_m", "difficulty", "created_at")
    list_filter = ("difficulty", "location")
    search_fields = ("title",)
    filter_horizontal = ("tags",)
    inlines = [ReviewInline]

# This allows managing trips directly from the admin interface
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("trail", "user", "rating", "created_at")
    list_filter = ("rating",)

# This allows managing trips directly from the admin interface
@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("user", "trail", "date")
    list_filter = ("date",)

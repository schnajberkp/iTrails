from django.contrib.auth.decorators import login_required 
from django.shortcuts import get_object_or_404, render, redirect 
from django.contrib import messages 
from .models import Trail, Review, Trip
from .forms import ReviewForm, TripForm 
from django.http import JsonResponse, HttpResponseBadRequest # For JSON responses and error handling
from django.db.models import Q # Allows complex queries (or, and, etc.)
from django.views.decorators.http import require_http_methods # For API views, to restrict methods like POST, GET, etc.

# List of all trails with basic info
def trail_list(request):
    trails = Trail.objects.order_by("-created_at")
    return render(request, "trails/trail_list.html", {"trails": trails})

# Detail view of a single trail, including reviews
def trail_detail(request, pk: int):
    "Detail trasy vcetne recenzi"
    trail = get_object_or_404(Trail, pk=pk)
    return render(request, "trails/trail_detail.html", {"trail": trail})

# Create a new review for a trail (only for logged-in users)
@login_required
def review_create(request, pk: int):
    trail = get_object_or_404(Trail, pk=pk)
    if Review.objects.filter(trail=trail, user=request.user).exists():
        messages.info(request, "Už jste tuto trasu ohodnotili.")
        return redirect("trail_detail", pk=trail.pk)
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.trail = trail
            review.user = request.user
            review.save()
            messages.success(request, "Recenze byla úspěšně přidána.")
            return redirect("trail_detail", pk=trail.pk)
    else:
        form = ReviewForm()
    # Render the review form for GET request
    return render(request, "trails/review_form.html", {"form": form, "trail": trail})

# List of trips for the logged-in user
@login_required
def my_trips(request):
    trips = Trip.objects.filter(user=request.user).order_by("-date")
    return render(request, "trails/trips_list.html", {"trips": trips})

# Create a new trip for the logged-in user (POST)
@login_required
def trip_create(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            messages.success(request, "Výlet byl úspěšně naplánován.")
            return redirect("my_trips")
    else:
        form = TripForm()
    return render(request, "trails/trip_form.html", {"form": form})


#---JSON API views---#

# Helper function to convert Trail model to dict for JSON output
def _trail_to_dict(trail):
    return {
        "id": trail.id,
        "title": trail.title,
        "location": {
            "id": trail.location.id,
            "name": trail.location.name,
            "country": trail.location.country,
            "region": trail.location.region,
        },
        "length_km": float(trail.length_km),
        "elevation_gain_m": trail.elevation_gain_m,
        "difficulty": trail.difficulty,
        "tags": [{"id": t.id, "name": t.name} for t in trail.tags.all()],
        "created_at": trail.created_at.isoformat(),
    }


# Returns a list of all trails in JSON format
#---- GET /api/trails/ ----

def trail_list_api(request):
    qs = Trail.objects.all().order_by("-created_at")

    q = request.GET.get("q")
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(location__name__icontains=q))

    mapping = {"easy":"EASY","moderate":"MODERATE","hard":"HARD",
            "EASY":"EASY","MODERATE":"MODERATE","HARD":"HARD"}
    diff = request.GET.get("difficulty")
    if diff in mapping:
        qs = qs.filter(difficulty=mapping[diff])

    data = [_trail_to_dict(trail) for trail in qs]
    return JsonResponse(data, safe=False)

# ---- GET /api/trail/<int:pk>/ ----
# Returns detail of a single trail in JSON format
def trail_detail_api(request, pk: int):
    trail = get_object_or_404(Trail, pk=pk)
    return JsonResponse(_trail_to_dict(trail))

# ---- GET /api/my_trips/ ---- (pouze prihlaseny uzivatel)
# Returns trips for the logged-in user in JSON format
@login_required
def my_trips_api(request):
    "Vrati vylety aktualniho uzivatele jako JSON"
    trips = Trip.objects.filter(user=request.user).order_by("-date")
    data = [{
        "id": t.id,
        "trail": {"id": t.trail.id, "title": t.trail.title},
        "date": t.date.isoformat(),
        "note": t.note,
    } for t in trips]
    return JsonResponse(data, safe=False)
    
# ---- POST /api/trail<int:pk>/reviews/ ---- (pouze prihlaseny uzivatel)
# Returns a new review for a trail in JSON format
@login_required
@require_http_methods(["POST"])
def review_create_api(request, pk: int):
    trail = get_object_or_404(Trail, pk=pk)

    # Check if user already reviewed this trail
    rating = request.POST.get("rating")
    comment = request.POST.get("comment", "")
    if rating is None and request.body:
        # Try to parse JSON body if no form data provided
        try:
            import json
            payload = json.loads(request.body.decode() or "{}")
            rating = payload.get("rating")
            comment = payload.get("comment", "")
        except Exception:
            return HttpResponseBadRequest("Invalid JSON format")
    try:
        rating = int(rating)
    except (ValueError, TypeError):
        return HttpResponseBadRequest("Rating must be an integer")
    
    if rating < 1 or rating > 5:
        return HttpResponseBadRequest("Rating must be between 1 and 5")
    
    # Prevent duplicate reviews
    if Review.objects.filter(trail=trail, user=request.user).exists():
        return JsonResponse({"ok": False, "error": "duplicate"}, status=400)
    
    # Create the review
    review = Review.objects.create(trail=trail, user=request.user, rating=rating, comment=comment)
    return JsonResponse({"ok": True, "id": review.id, "created_at": review.created_at.isoformat()})
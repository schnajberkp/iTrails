import pytest
from datetime import date
from django.urls import reverse
from trails.models import Trip

# Test access control and functionality of the "My Trips" view
@pytest.mark.django_db
def test_my_trips_requires_login(client):
    resp = client.get(reverse("my_trips"))
    assert resp.status_code in (301, 302)
    assert "/accounts/login/" in resp.headers.get("Location", "")

# Login and access the view
@pytest.mark.django_db
def test_my_trips_shows_only_user_trips(client, user, trail, django_user_model):
    other = django_user_model.objects.create_user(username="other", password="x")

    # Create trips for both users
    my_trip = Trip.objects.create(user=user, trail=trail, date=date(2025, 8, 20), note="Můj výlet")
    Trip.objects.create(user=other, trail=trail, date=date(2025, 8, 21), note="Cizí výlet")

    # Login as 'user' and access the view
    client.login(username="testuser", password="12345")
    resp = client.get(reverse("my_trips"))
    assert resp.status_code == 200

    # Check that only 'user's trip is in the context
    trips_in_ctx = resp.context["trips"]
    assert trips_in_ctx.count() == 1
    t = trips_in_ctx.first()
    assert t.id == my_trip.id
    assert t.user == user
    assert t.trail == trail
    assert t.date == date(2025, 8, 20)

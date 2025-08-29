import pytest
from django.urls import reverse
from trails.models import Trip

# Test access control and functionality of the "Trip Create" view
@pytest.mark.django_db
def test_trip_create_requires_login(client):
    """Nepřihlášený uživatel se nedostane na stránku – redirect na login."""
    resp = client.get(reverse("trip_create"))
    assert resp.status_code in (301, 302)
    assert "/accounts/login/" in resp.headers.get("Location", "")

# Login and access the view
@pytest.mark.django_db
def test_trip_create_post_ok(client, user, trail):
    """Přihlášený uživatel může vytvořit nový výlet."""
    client.login(username="testuser", password="12345")
    resp = client.post(
        reverse("trip_create"),
        {"trail": trail.id, "date": "2025-08-21", "note": "Test výlet"},
        follow=True,
    )
    assert resp.status_code == 200
    assert Trip.objects.filter(user=user, trail=trail, date="2025-08-21").exists()

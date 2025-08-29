import pytest
from django.urls import reverse
from trails.models import Review

# Test access control and functionality of the "Create Review" view
@pytest.mark.django_db
def test_review_create_requires_login(client, trail):
    url = reverse("review_create", args=[trail.id])
    resp = client.get(url)
    # Redirect to login 
    assert resp.status_code in (302, 301)
    assert "/accounts/login/" in resp.headers.get("Location", "")

# Login and access the view
@pytest.mark.django_db
def test_review_create_post_ok_for_logged_user(client, user, trail):
    client.login(username="testuser", password="12345")
    url = reverse("review_create", args=[trail.id])
    data = {"rating": 5, "comment": "Parádní trasa!"}
    resp = client.post(url, data, follow=True)
    assert resp.status_code == 200
    # Review by "testuser" for this trail exists
    assert Review.objects.filter(trail=trail, user__username="testuser", rating= 5).exists()

# Prevent duplicate reviews by the same user for the same trail
@pytest.mark.django_db
def test_review_create_prevents_duplicate_review(client, user, trail):
    client.login(username="testuser", password="12345")
    url = reverse("review_create", args=[trail.id])
    client.post(url, {"rating": 4, "comment": "ok"}, follow=True)
    client.post(url, {"rating": 5, "comment": "Skvělá trasa!"}, follow=True)
    assert Review.objects.filter(trail=trail, user=user).count() == 1


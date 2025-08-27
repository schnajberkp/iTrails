import pytest
from django.urls import reverse
from trails.models import Review

@pytest.mark.django_db
def test_review_create_requires_login(client, trail):
    url = reverse("review_create", args=[trail.id])
    resp = client.get(url)
    # Redirect to login 
    assert resp.status_code in (302, 301)
    assert "/accounts/login/" in resp.headers.get("Location", "")

@pytest.mark.django_db
def test_review_create_post_ok_for_logged_user(client, user, trail):
    client.login(username="tester", password="12345")
    url = reverse("review_create", args=[trail.id])
    data = {"rating": 5, "comment": "Parádní trasa!"}
    resp = client.post(url, data, follow=True)
    assert resp.status_code == 200
    # Review by 'tester' for this trail exists
    assert Review.objects.filter(trail=trail, user__username="tester", rating= 5).exists()

@pytest.mark.django_db
def test_review_create_prevents_duplicate_review(client, user, trail):
    client.login(username="tester", password="12345")
    url = reverse("review_create", args=[trail.id])
    client.post(url, {"rating": 4, "comment": "ok"}, follow=True)
    # Second attempt should redirect with info message
    client.post(url, {"rating": 5, "comment": "Skvělá trasa!"}, follow=True)
    from django.contrib.auth.models import User
    u = User.objects.get(username="tester")
    assert Review.objects.filter(trail=trail, user=u).count() == 1
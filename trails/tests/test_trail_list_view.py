import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_trail_list_status_code(client):
    url = reverse('trail_list')
    resp = client.get(url)
    assert resp.status_code == 200

@pytest.mark.django_db
def test_trail_list_contains_trail_title(client, trail):
    url = reverse('trail_list')
    resp = client.get(url)
    assert resp.status_code == 200
    assert trail.title in resp.content.decode()
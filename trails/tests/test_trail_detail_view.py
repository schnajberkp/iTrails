import pytest
from django.urls import reverse

# Test access control and functionality of the "Trail Detail" view
@pytest.mark.django_db
def test_trail_detail_200(client, trail):
    url = reverse("trail_detail", args=[trail.id])
    resp = client.get(url)
    assert resp.status_code == 200
    assert trail.title in resp.content.decode()

# Login is not required to view trail details
@pytest.mark.django_db
def test_trail_detail_404_for_unknown(client):
    url = reverse("trail_detail", args=[9999])
    resp = client.get(url)
    assert resp.status_code == 404
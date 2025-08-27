import pytest
from django.contrib.auth.models import User
from trails.models import Location, Trail

@pytest.fixture
def user(db):
    return User.objects.create_user(username="tester", password="12345")

@pytest.fixture
def location(db):
    return Location.objects.create(name="Test Location", country="Czech Republic", region="Test Region")

@pytest.fixture
def trail(db, location):
    return Trail.objects.create(
        title="Test Trail",
        location=location,
        length_km=5.0,
        elevation_gain_m=100,
        difficulty="moderate"
    )




import pytest
from django.contrib.auth.models import User
from trails.models import Location, Trail

# Fixtures for creating test data
@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="12345")

# Fixture for creating a Location
@pytest.fixture
def location(db):
    return Location.objects.create(name="Test Location", country="Czech Republic", region="Test Region")

# Fixture for creating a Trail
@pytest.fixture
def trail(db, location):
    return Trail.objects.create(
        title="Test Trail",
        location=location,
        length_km=5.0,
        elevation_gain_m=100,
        difficulty="MODERATE"
    )




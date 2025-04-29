import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse
from jose import jwt
from tasks.utils import SECRET_KEY, ALGORITHM  # Adjust if stored elsewhere

@pytest.mark.django_db
def test_protected_route_with_valid_token():
    user = User.objects.create_user(username="jwtuser", password="jwtpass")
    token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm=ALGORITHM)

    client = APIClient()
    client.cookies['jwt_token'] = token  # Simulate Django session behavior

    response = client.get(reverse("task-list"))

    assert response.status_code == 200 or response.status_code == 302  # Depending on login redirect

@pytest.mark.django_db
def test_protected_route_with_invalid_token():
    client = APIClient()
    client.cookies['jwt_token'] = "invalid.token.string"

    response = client.get(reverse("task-list"))
    assert response.status_code == 302
    assert "/login" in response.url

@pytest.mark.django_db
def test_protected_route_without_token():
    client = APIClient()
    response = client.get(reverse("task-list"))

    assert response.status_code == 302
    assert "/login" in response.url

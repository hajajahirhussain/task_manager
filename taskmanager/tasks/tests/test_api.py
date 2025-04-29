import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from tasks.models import Task
from django.urls import reverse

@pytest.mark.django_db
def test_task_list_api():
    user = User.objects.create_user(username="apitester", password="testpass")
    Task.objects.create(title="API Task 1", user=user)
    Task.objects.create(title="API Task 2", user=user)

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("api-task-list")
    response = client.get(url)

    assert response.status_code == 200
    # assert len(response.data) == 2 not work because of upagination
    assert len(response.data["results"]) == 2
    # assert response.data[0]["title"] == "API Task 1" not work because of the pagination
    titles = [task["title"] for task in response.data["results"]]
    assert "API Task 1" in titles
    assert "API Task 2" in titles
    
    '''
    # tasks/tests/test_api.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from tasks.models import Task
from django.contrib.auth.models import User

class TaskAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apitester", password="testpass")
        Task.objects.create(title="API Task 1", user=self.user)
        Task.objects.create(title="API Task 2", user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_task_list_api(self):
        url = reverse("api-task-list")  # adjust to your actual DRF url name
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response..data["results"]), 2)
        #self.assertEqual(response.data[0]["title"], "API Task 1")
        titles = [task["title"] for task in response.data["results"]]
        self.assertIn("API Task 1", titles)
        self.assertIn("API Task 2", titles)
    '''

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from tasks.models import Task
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_task_create_api():
    user = User.objects.create_user(username="apicreater", password="testpass", is_staff=True)
    
    data = {
        "title": "API Task 1",
        "user": user.id
    }
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("api-task-list")
    response = client.post(url, data)

    assert response.status_code == 201  # POST creates, so should be 201 Created
    assert response.data["title"] == "API Task 1"
    assert Task.objects.filter(title="API Task 1", user=user).exists()


@pytest.mark.django_db
def test_task_update_api():
    user = User.objects.create_user(username="apiediter", password="testpass", is_staff=True)
    task = Task.objects.create(title="API Task 1", user=user)

    data = {
        "title": "API Task 3",
        "user": user.id,
        "description": "Updated description",  # Include any required fields
    }

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("api-task-detail", args=[task.id])
    response = client.put(url, data)

    assert response.status_code == 200  # ✅ PUT returns 200 if successful
    assert response.data["title"] == "API Task 3"
    assert Task.objects.filter(title="API Task 3", user=user).exists()


@pytest.mark.django_db
def test_task_delete_api():
    user = User.objects.create_user(username="apieraser", password="testpass", is_staff=True)
    task = Task.objects.create(title="API Task 1", user=user)

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("api-task-detail", args=[task.id])
    response = client.delete(url)

    
    assert response.status_code == 204 
    assert Task.objects.count() == 0
    assert not Task.objects.filter(title="API Task 1", user=user).exists()

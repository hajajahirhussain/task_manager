from django.test import TestCase
from tasks.models import Task, AdminLog, User
from tasks.serializers import TaskSerializer, AdminLogSerializer

class TaskSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ser_user", password="testpass")
        self.task_data = {
            "title": "Test Task",
            "description": "Test description",
            "completed": False,
            "user": self.user.id
        }

    def test_task_serializer_valid(self):
        serializer = TaskSerializer(data=self.task_data)
        self.assertTrue(serializer.is_valid())

    def test_task_serializer_invalid_missing_title(self):
        data = self.task_data.copy()
        data.pop("title")
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_task_serializer_save(self):
        serializer = TaskSerializer(data=self.task_data)
        self.assertTrue(serializer.is_valid())
        task = serializer.save()
        self.assertEqual(task.title, self.task_data["title"])
        self.assertEqual(task.user, self.user)


class AdminLogSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="adminuser", password="adminpass")
        self.task = Task.objects.create(title="Some Task", user=self.user)
        self.log_data = {
            "admin": self.user.id,
            "action": "created",
            "task": self.task.id
        }

    def test_admin_log_serializer_valid(self):
        serializer = AdminLogSerializer(data=self.log_data)
        self.assertTrue(serializer.is_valid())

    def test_admin_log_serializer_invalid_missing_action(self):
        data = self.log_data.copy()
        data.pop("action")
        serializer = AdminLogSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("action", serializer.errors)



'''### UNITTEST VERSION ###


import pytest
from tasks.serializers import TaskSerializer
from tasks.models import User

@pytest.mark.django_db
def test_task_serializer_valid_data():
    user = User.objects.create_user(username="serializeruser", password="pass123")
    data = {
        "title": "Serialized Task",
        "description": "Test description",
        "completed": False,
        "user": user.id,
    }
    serializer = TaskSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data["title"] == "Serialized Task"

@pytest.mark.django_db
def test_task_serializer_missing_title():
    user = User.objects.create_user(username="serializeruser2", password="pass123")
    data = {
        "description": "No title",
        "completed": False,
        "user": user.id,
    }
    serializer = TaskSerializer(data=data)
    assert not serializer.is_valid()
    assert "title" in serializer.errors
'''

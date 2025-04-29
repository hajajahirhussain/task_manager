# import pytest
# from django.contrib.auth.models import User, AnonymousUser
# from rest_framework.test import APIRequestFactory
# from tasks.models import Task
# from tasks.permissions import IsOwnerOrAdmin
# from rest_framework.permissions import SAFE_METHODS


# @pytest.mark.django_db
# def test_admin_can_modify_any_task():
#     factory = APIRequestFactory()
#     admin = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
#     user = User.objects.create_user(username="user", password="userpass")
#     task = Task.objects.create(title="User Task", user=user)

#     request = factory.delete("/fake-url/")
#     request.user = admin

#     permission = IsOwnerOrAdmin()
#     assert permission.has_object_permission(request, None, task) is True


# @pytest.mark.django_db
# def test_owner_can_modify_own_task():
#     factory = APIRequestFactory()
#     user = User.objects.create_user(username="user", password="userpass")
#     task = Task.objects.create(title="User Task", user=user)

#     request = factory.put("/fake-url/")
#     request.user = user

#     permission = IsOwnerOrAdmin()
#     assert permission.has_object_permission(request, None, task) is True


# @pytest.mark.django_db
# def test_other_user_cannot_modify_task():
#     factory = APIRequestFactory()
#     owner = User.objects.create_user(username="owner", password="ownerpass")
#     other = User.objects.create_user(username="other", password="otherpass")
#     task = Task.objects.create(title="Owner Task", user=owner)

#     request = factory.delete("/fake-url/")
#     request.user = other

#     permission = IsOwnerOrAdmin()
#     assert permission.has_object_permission(request, None, task) is False


# @pytest.mark.django_db
# def test_any_user_can_read():
#     factory = APIRequestFactory()
#     owner = User.objects.create_user(username="owner", password="ownerpass")
#     task = Task.objects.create(title="Read Task", user=owner)

#     request = factory.get("/fake-url/")
#     request.user = AnonymousUser()

#     permission = IsOwnerOrAdmin()
#     assert permission.has_object_permission(request, None, task) is True


import unittest
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from tasks.models import Task
from tasks.permissions import IsOwnerOrAdmin


class TestIsOwnerOrAdmin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(username="owner", password="ownerpass")
        self.other = User.objects.create_user(username="other", password="otherpass")
        self.admin = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
        self.task = Task.objects.create(title="Test Task", user=self.owner)
        self.permission = IsOwnerOrAdmin()

    def test_admin_can_modify_any_task(self):
        request = self.factory.put("/fake-url/")
        request.user = self.admin
        self.assertTrue(self.permission.has_object_permission(request, None, self.task))

    def test_owner_can_modify_own_task(self):
        request = self.factory.put("/fake-url/")
        request.user = self.owner
        self.assertTrue(self.permission.has_object_permission(request, None, self.task))

    def test_other_user_cannot_modify_task(self):
        request = self.factory.delete("/fake-url/")
        request.user = self.other
        self.assertFalse(self.permission.has_object_permission(request, None, self.task))

    def test_any_user_can_read(self):
        request = self.factory.get("/fake-url/")
        request.user = AnonymousUser()
        self.assertTrue(self.permission.has_object_permission(request, None, self.task))

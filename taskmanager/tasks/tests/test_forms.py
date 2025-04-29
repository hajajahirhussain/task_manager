import pytest
from tasks.forms import TaskForm
from tasks.models import Task
from django.contrib.auth.models import User
from datetime import date

@pytest.mark.django_db
def test_task_form_valid():
    user = User.objects.create_user(username="formtester", password="pass1234")
    form_data = {
        "title": "Test Task",
        "description": "This is a task created in a form test",
        "start_date": date.today(),
        "end_date": date.today(),
        "completed": False,
        "user": user.id
    }
    form = TaskForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_task_form_missing_title():
    user = User.objects.create_user(username="formtester2", password="pass1234")
    form_data = {
        # Missing title
        "description": "Missing title test",
        "start_date": date.today(),
        "end_date": date.today(),
        "completed": False,
        "user": user.id
    }
    form = TaskForm(data=form_data)
    assert not form.is_valid()
    assert "title" in form.errors

import pytest
from tasks.models import Task, AdminLog
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_create_task():
    # Arrange (Setup test data)
    user = User.objects.create_user(username="testuser", password="testpass")
    
    # Act (Action)
    task = Task.objects.create(
        title="Test Task",
        description="This is a test task.",
        user=user
    )

    # Assert (Verification)
    assert task.title == "Test Task"
    assert task.description == "This is a test task."
    assert task.completed == False  # default value
    assert task.user.username == "testuser"




@pytest.mark.django_db
def test_create_admin_log():
    admin = User.objects.create_user(username="adminuser", password="adminpass")
    task = Task.objects.create(user=admin, title="Test Task", description="Some details")

    log = AdminLog.objects.create(
        admin=admin,
        task=task,
        action="Created Task"
    )

    assert log.id is not None
    assert log.admin == admin
    assert log.task == task
    assert log.action == "Created Task"
    assert log.timestamp is not None
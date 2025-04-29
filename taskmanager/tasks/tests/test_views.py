# import pytest
# from django.urls import reverse
# from django.contrib.auth.models import User
# from tasks.models import Task

# import jwt
# from django.conf import settings

# def create_jwt_token(username):
#     payload = {"sub": username}
#     return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

# @pytest.mark.django_db
# def test_task_list_view(client):
#     user = User.objects.create_user(username="viewuser", password="pass123")
#     Task.objects.create(title="User Task 1", user=user)
#     Task.objects.create(title="User Task 2", user=user)

#     client.session['jwt_token'] = create_jwt_token("viewuser")
#     response = client.get(reverse("task-list"))

#     assert response.status_code == 200
#     assert "User Task 1" in response.content.decode()
#     assert "User Task 2" in response.content.decode()


# @pytest.mark.django_db
# def test_task_list_view_redirects_for_anonymous(client):
#     response = client.get(reverse("task-list"))
#     assert response.status_code == 302
#     assert "/login" in response.url


# @pytest.mark.django_db
# def test_add_task_view(client):
#     user = User.objects.create_user(username="adder", password="pass123")
#     client.session['jwt_token'] = create_jwt_token("adder")

#     response = client.post(reverse("add-task"), {
#         "title": "New Test Task",
#         "description": "A test task for adding.",
#     })

#     assert response.status_code == 200 or response.status_code == 302
#     assert Task.objects.filter(title="New Test Task", user=user).exists()


# @pytest.mark.django_db
# def test_update_task_view(client):
#     user = User.objects.create_user(username="editor", password="pass123")
#     task = Task.objects.create(title="Old Title", user=user)

#     client.session['jwt_token'] = create_jwt_token("editor")


#     response = client.post(reverse("edit-task", args=[task.id]), {
#         "title": "Updated Title",
#         "description": "Updated Description",
#     })

#     task.refresh_from_db()
#     assert response.status_code == 302
#     assert task.title == "Updated Title"


# @pytest.mark.django_db
# def test_delete_task_view(client):
#     user = User.objects.create_user(username="deleter", password="pass123")
#     task = Task.objects.create(title="To Be Deleted", user=user)

#     client.session['jwt_token'] = create_jwt_token("deleter")
#     client.session.save()

#     response = client.post(reverse("delete-task", args=[task.id]))

#     assert response.status_code == 302
#     assert not Task.objects.filter(id=task.id).exists()

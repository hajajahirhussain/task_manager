
# 1 GET Request (Retrieve Data)
# import requests
#
# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyMTAzMzczLCJpYXQiOjE3NDIwNDgzMDQsImp0aSI6ImRjZWQ1NGY3ZGMzNjQ0NzA4MTRhZWFmNGMzYjY1NTVjIiwidXNlcl9pZCI6Mn0.DxdybToSk5pc5-Lif9owF8DmJOfMsdxXUydUSKFB54Y"  # Your access token
# }
#
# response = requests.get("http://127.0.0.1:8000/api/tasks/", headers=headers)
# print(response.json())  # Should return your tasks
#
# # POST Request (Create a New Task)
# import requests
#
# headers = {
#     "Authorization": "Bearer YOUR_ACCESS_TOKEN",
#     "Content-Type": "application/json"
# }
#
# data = {
#     "title": "New Task",
#     "description": "This is a test task",
#     "completed": False
# }
#
# response = requests.post("http://127.0.0.1:8000/api/tasks/create/", json=data, headers=headers)
# print(response.json())  # Should return the newly created task

# 3 PUT Request (Update an Existing Task)

# import requests
#
# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyMTEyNzY3LCJpYXQiOjE3NDIwNDgzMDQsImp0aSI6ImI1MzJjZGQ0YWYzODQyMzRiMzIxOWYwMzU5NTk0MDdkIiwidXNlcl9pZCI6Mn0.USMzaF37jsE_pddACzWjSnSWkA0cPbcgxr5dhSKzoxs",  # Your access token,
#     "Content-Type": "application/json"
# }
#
# data = {
#     "title": "Updated Task",
#     "description": "Updated details",
#     "completed": True
# }
#
# task_id = 15  # Change to the ID of the task you want to update
# response = requests.put(f"http://127.0.0.1:8000/api/tasks/{task_id}/update/", json=data, headers=headers)
# print(response.json())  # Should return the updated task details


# 4 DELETE Request (Remove a Task)
#
# import requests
#
# headers = {
#     "Authorization": "Bearer YOUR_ACCESS_TOKEN"
# }
#
# task_id = 1  # Change to the ID of the task you want to delete
# response = requests.delete(f"http://127.0.0.1:8000/api/tasks/{task_id}/delete/", headers=headers)
#
# if response.status_code == 204:
#     print("Task deleted successfully!")
# else:
#     print(response.json())  # If any error occurs


''' Common Issues & Fixes
401 Unauthorized: Ensure your JWT token is valid and not expired.
403 Forbidden: Your user might not have the required permissions.
404 Not Found: Check if the task ID exists before updating/deleting.
400 Bad Request: Ensure you send valid JSON data for POST/PUT.
'''

import requests

def get_headers():
    """Return headers with the latest access token."""
    return {"Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"}

def refresh_access_token():
    """Request a new access token using the refresh token."""
    global ACCESS_TOKEN  # Update global variable
    response = requests.post(REFRESH_URL, json={"refresh": REFRESH_TOKEN})
    if response.status_code == 200:
        ACCESS_TOKEN = response.json()["access"]
        print("🔄 Token refreshed successfully!")
    else:
        print("❌ Failed to refresh token:", response.json())

def get_tasks():
    """Fetch tasks with auto-refresh on token expiry."""
    global ACCESS_TOKEN  # Access the updated token

    data = {
        "title": "Updated Task",
    "description": "modified",
    "completed": 'false',
    "user": 1

}

    if requests.get(TASKS_URL,  headers=get_headers()).status_code == 401:  # Token expired
        print("⚠️ Token expired! Refreshing...")
        refresh_access_token()
        # response = requests.get(TASKS_URL, headers=get_headers())  # Retry with new token
        print(ACCESS_TOKEN)

    # response = requests.put(TASKS_URL,json=data,  headers=get_headers())
    response = requests.get(TASKS_URL, headers=get_headers())
    return response.json()

# Your tokens
# ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyMzg1NDIzLCJpYXQiOjE3NDIzODUxMjMsImp0aSI6IjMxMjBhZTBjZjU2NjQwMTY4MjcxODE2NWJlYjI2ZjI3IiwidXNlcl9pZCI6Mn0.Xb4B4twGTO_f0ggfM_7vlC-rwT3BUFByoZhYoxXdW9g"
# REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MjQ3MTUyMywiaWF0IjoxNzQyMzg1MTIzLCJqdGkiOiIyZWExYTFkMGE4MDY0OWRhYmZiNjdiM2JiMTlkMGU2NSIsInVzZXJfaWQiOjJ9.eujftN-r7vBR0H7bxPk0N9xeM8ET_SRlAQhXXY_4tIg"
#Admin
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyMzkyNDA4LCJpYXQiOjE3NDIzODM2MDMsImp0aSI6IjA0MmJjZjA5MGNmMjQ4MDA4OTk5Y2RhZDRkMWRiNjQxIiwidXNlcl9pZCI6MX0.fyffKDmLdsX-VHKAZv3ef2WhWSN_77Dm4HVFf1jmeTw"
REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MjQ3MDAwMywiaWF0IjoxNzQyMzgzNjAzLCJqdGkiOiI1ODZlNDc0M2M2NjI0NThlODJmOTAyOTkxZDgzMTU3NiIsInVzZXJfaWQiOjF9.bKBshbsuuRXPZyNkirMchpDsMAHpqRlgO34lNrrazkc"
# API Endpoints
task_id = 22  # Change to the ID of the task you want to update
# TASKS_URL = f"http://127.0.0.1:8000/api/tasks/{task_id}/" #"http://127.0.0.1:8000/api/tasks/"
TASKS_URL = "http://127.0.0.1:8000/api/tasks/"
REFRESH_URL = "http://127.0.0.1:8000/api/token/refresh/"
# update_task()
# Run API Call
tasks = get_tasks()
print(tasks)
django_questin_answers =  "https://chatgpt.com/canvas/shared/67d96a6427a881918c194707d3336480"

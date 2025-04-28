from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
# from .models import Task
from .models import Task, AdminLog  
from .forms import TaskForm  # Import the form
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
from django.db.models import Q  # ✅ Add this import
from django.contrib.auth.models import User
from django.core.paginator import Paginator
#API
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TaskSerializer, AdminLogSerializer
from rest_framework import status
#JWT
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework import viewsets, permissions
from .permissions import IsAdminOrReadOnly  # Import the new permission
from .permissions import IsOwnerOrAdmin  # Import the new permission
#Logging - Admin
# import logging
# logger = logging.getLogger('django')
# from rest_framework.permissions import IsAdminUser
#Filtering
from django_filters.rest_framework import DjangoFilterBackend
#Throttles
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from tasks.throttles import AdminRateThrottle  # Import custom throttle

#FastAPI
import requests
# from django.shortcuts import render, redirect
# from django.contrib import messages
from django.conf import settings
from .forms import LoginForm
from django.utils.http import url_has_allowed_host_and_scheme
from .utils import jwt_login_required
FASTAPI_LOGIN_URL = f"{settings.FASTAPI_AUTH_URL}/login"
FASTAPI_REGISTER_URL = f"{settings.FASTAPI_AUTH_URL}/register"
from django.contrib.auth import authenticate

class TaskViewSet(viewsets.ModelViewSet):   
    # queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # permission_classes = [permissions.IsAuthenticated] # Apply custom permission
    permission_classes =  [IsAdminOrReadOnly]  # Admin can do anything others only view
    # permission_classes = [IsOwnerOrAdmin]  # Admin can do anything others only change their own task
    # Add filtering
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['completed', 'start_date', 'end_date']  # Fields for filtering
    
    # Apply throttles (Admin first)
    # throttle_classes = [AdminRateThrottle, UserRateThrottle, AnonRateThrottle]
    def get_throttles(self):
        """Apply different throttles based on user type"""
        if self.request.user.is_staff:
            return [AdminRateThrottle()]  # Admin gets 10/min
        elif self.request.user.is_authenticated:
            return [UserRateThrottle()]  # Normal user gets 5/min
        else:
            return [AnonRateThrottle()]  # Anonymous user gets 3/min
        
    def get_queryset(self):
        # If the user is an admin, show all tasks
        if self.request.user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)  # Ensure new tasks are assigned to the logged-in user

    def perform_create(self, serializer):
        assigned_user_id = self.request.data.get("user")  # Get user ID from request data
        if assigned_user_id:
            try:
                assigned_user = User.objects.get(id=assigned_user_id)  # Fetch user instance
            except User.DoesNotExist:
                raise serializers.ValidationError({"user": "User does not exist"})  # Handle invalid user
        else:
            assigned_user = self.request.user  # Default to the logged-in user

        task = serializer.save(user=assigned_user)  # Assign the correct user
        if self.request.user.is_staff:  # Only log if admin
            AdminLog.objects.create(
                admin=self.request.user, action="Created Task", task=task
            )

    def list(self, request, *args, **kwargs):
        print(f"User: {request.user.username}, Is Admin: {request.user.is_staff}")
        return super().list(request, *args, **kwargs)
    

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if request.user.is_staff:  # Only log if admin
            task = self.get_object()  # Get the task instance
            AdminLog.objects.create(
                admin=request.user, action="Updated Task", task=task  # Use task object, not task_id
            )
        return response

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()  # Fetch the task before deleting
        if request.user.is_staff:
            AdminLog.objects.create(
                admin=request.user, action="Deleted Task", task=task  # Use task instance
            )
        return super().destroy(request, *args, **kwargs)
    # Add this line to avoid the assertion error
    # queryset = Task.objects.none()  # Prevents Django from complaining

class AdminLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdminLog.objects.all()
    serializer_class = AdminLogSerializer
    permission_classes = [IsAdminUser]

# @login_required
@jwt_login_required
def task_list(request):
    user = User.objects.filter(username=request.username).first()
    if not user:
        raw_password = request.session.get('raw_password', 'temp')  # fallback to "temp" just in case
        user = User.objects.create_user(username=request.username, password=raw_password)
        # password won’t be used since auth is handled via FastAPI
        user.save()
        # messages.error(request, "User not found in Django DB.")
        # return redirect("login")
        del request.session['raw_password']
    tasks = Task.objects.filter(user=user)
    # tasks = Task.objects.filter(user=request.user) # Show only tasks of logged-in user

     # 🔍 Search Functionality
    search_query = request.GET.get("search", "")
    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    
    # ✅ Filter: Show Completed or Pending Tasks
    filter_status = request.GET.get("status", "")
    if filter_status == "completed":
        tasks = tasks.filter(completed=True)
    elif filter_status == "pending":
        tasks = tasks.filter(completed=False)

    # 🔽 Sorting by Title, Start Date, or End Date
    sort_by = request.GET.get("sort", "start_date")  # Get sort parameter, default to "start_date"
    if sort_by in ["title", "start_date", "end_date"]:
        if sort_by == "start_date":  # Ensure descending order for default
            sort_by = "-start_date"
        tasks = tasks.order_by(sort_by)

    # 🟢 Pagination: Show 10 tasks per page
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/task_list.html', {
        'tasks': page_obj,  # Pass paginated tasks
        "search_query": search_query,
        "filter_status": filter_status,
        "sort_by": sort_by,
        "page_obj": page_obj,  # Pass pagination object
        "user": user,  # inject manually
    })

    # return render(request, 'tasks/task_list.html', {'tasks' : tasks, "search_query": search_query, "filter_status": filter_status, "sort_by": sort_by})


# @login_required
@jwt_login_required
def add_task(request):
    user = User.objects.filter(username=request.username).first()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task_title = form.cleaned_data.get('title', None)  
            if task_title and Task.objects.filter(title=task_title).exists():  # Check for existing task
                messages.error(request, "The task title already exists.")  # Show error
            else:
                task = form.save(commit=False)  # Don't save yet
                # task.user = request.user  # Assign the logged-in user
                task.user = user  # Assign the logged-in user
                task.save()  # Now save the task
                # return redirect('task-list')  # Redirect to the task list page
                messages.success(request, "Task added successfully!")  # Show a success message
                form = TaskForm()
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {
        'form': form,"user": user, # inject manually
    })


# @login_required
@jwt_login_required
def update_task(request, task_id):
    user = User.objects.filter(username=request.username).first()
    task = get_object_or_404(Task, id=task_id, user=user)  # Fetch the task or return 404 # Ensure user owns the task

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect('task-list')  # Redirect back to the task list

    else:
        form = TaskForm(instance=task)  # Pre-fill form with task data

    return render(request, 'tasks/edit_task.html', {'form': form, "user": user, # inject manually
                                                   })

# @login_required
@jwt_login_required
def delete_task(request, task_id):
    user = User.objects.filter(username=request.username).first()
    task = get_object_or_404(Task, id=task_id, user=user)  # Ensure user owns the task # Fetch the task or return 404
    
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('task-list')

    return render(request, 'tasks/confirm_delete.html', {'task': task,"user": user, # inject manually
                                                   })

# @login_required
@jwt_login_required
def complete_task(request, task_id):
    user = User.objects.filter(username=request.username).first()
    task = get_object_or_404(Task, id=task_id, user=user)  # Ensure user owns the task
    task.completed = True  # Mark as completed
    task.save()
    return redirect('task-list')  # Redirect back to the task list


# @api_view(['GET', 'POST'])  # Allow both GET and POST requests
@jwt_login_required
@api_view(['GET'])  # Allow both GET and POST requests
@permission_classes([IsAuthenticated])  # 🔒 Require JWT token
def task_list_api(request):
    if request.method == 'GET':  #GET (List all tasks)
        user = User.objects.filter(username=request.username).first()
        # 🟢 Fetch all tasks (existing logic)
        tasks = Task.objects.filter(user=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    # elif request.method == 'POST':  # POST (Create a new task)
    #     # 🔴 Create a new task
    #     serializer = TaskSerializer(data=request.data)  
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)  # Assign the logged-in user
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 🔒 Require JWT token
def task_create_api(request): #POST (Create a new task)
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # Assign the logged-in user
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return the created task
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 🔒 Require JWT token
def task_detail_api(request, task_id): #GET (Retrieve a single task)
    try:
        task = Task.objects.get(id=task_id, user=request.user)  # Get the task for the logged-in user
        serializer = TaskSerializer(task)
        return Response(serializer.data)  # Return JSON response
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # 🔒 Require JWT token
def task_update_api(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)  # Get task for logged-in user
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task, data=request.data, partial=True)  # Allow partial updates
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)  # Return updated task
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # 🔒 Require JWT token
def task_delete_api(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)  # Get task for logged-in user
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    task.delete()  # Delete the task
    return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Django user created
            # login(request, user)  # Optional: log in right away

            # Register same user in FastAPI
            try:
                response = requests.post(
                    FASTAPI_REGISTER_URL,
                    json={
                        "username": user.username,
                        "password": request.POST.get("password1")
                    }
                )
                if response.status_code == 200:
                    messages.success(request, "Registered in both systems successfully.")
                else:
                    messages.warning(request, "Django user created, but FastAPI registration failed.")
            except Exception as e:
                messages.warning(request, f"FastAPI registration error: {e}")

            return redirect("task-list")
    else:
        form = UserCreationForm()

    return render(request, "tasks/register.html", {"form": form})




# def custom_login(request):
#     next_url = request.GET.get("next", "/")  # Get ?next=...
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             # email = form.cleaned_data['email']
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             try:
#                 response = requests.post(
#                     FASTAPI_LOGIN_URL,
#                     # data={"username": email, "password": password}
#                     data={"username": username, "password": password}
#                 )
#                 if response.status_code == 200:
#                     token = response.json()["access_token"]
#                     request.session['jwt_token'] = token
#                     request.session['raw_password'] = password  # 🆕 store password
#                     messages.success(request, "Login successful!")
#                     # Safely redirect to next (default to task-list)
#                     if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
#                         print("Redirecting to(next):", redirect(next_url))
#                         return redirect(next_url)
#                     print("Redirecting to(direct):", redirect("task-list"))
#                     return redirect("task-list")
#                 else:
#                     messages.error(request, "Invalid credentials.")
#             except Exception as e:
#                 messages.error(request, f"Error: {e}")
#     else:
#         form = LoginForm()
    
#     return render(request, "tasks/login.html", {"form": form})

def custom_login(request):
    next_url = request.GET.get("next", "/")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                # 🔐 Step 1: Try FastAPI login
                response = requests.post(FASTAPI_LOGIN_URL, data={
                    "username": username,
                    "password": password
                })

                # ✅ Login success
                if response.status_code == 200:
                    token = response.json()["access_token"]
                    request.session['jwt_token'] = token
                    messages.success(request, "Login successful!")
                    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                        return redirect(next_url)
                    return redirect("task-list")

                # ❌ FastAPI login failed — try registering
                elif response.status_code == 400:
                    # Check if user exists in Django and password matches
                    user = authenticate(username=username, password=password)
                    if user:
                        # 🔄 Step 2: Register to FastAPI
                        reg_res = requests.post(FASTAPI_REGISTER_URL, json={
                            "username": username,
                            "password": password
                        })

                        # ✅ Step 3: Retry login
                        if reg_res.status_code == 200:
                            retry_login = requests.post(FASTAPI_LOGIN_URL, data={
                                "username": username,
                                "password": password
                            })
                            if retry_login.status_code == 200:
                                token = retry_login.json()["access_token"]
                                request.session['jwt_token'] = token
                                messages.success(request, "Login successful!")
                                if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                                    return redirect(next_url)
                                return redirect("task-list")
                            else:
                                messages.error(request, "Login retry failed after FastAPI registration.")
                        else:
                            messages.error(request, "FastAPI registration failed.")

                    else:
                        messages.error(request, "Invalid credentials or user does not exist in Django.")

                else:
                    messages.error(request, "Unexpected error from FastAPI.")

            except Exception as e:
                messages.error(request, f"Error: {e}")

    else:
        form = LoginForm()

    return render(request, "tasks/login.html", {"form": form})


def custom_logout(request):
    request.session.flush()  # ✅ Clears JWT and any session data
    messages.success(request, "You’ve been logged out successfully.")
    return redirect("login")
from django.urls import path,include
# from .views import task_list, add_task, update_task, delete_task, complete_task, register
# from .views import  task_list_api, task_create_api, task_detail_api, task_update_api, task_delete_api     
from .views import (
    task_list, add_task, update_task, delete_task, complete_task, register,
    TaskViewSet, AdminLogViewSet
)
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
# from .views import TaskViewSet, AdminLogViewSet


# Create a router and register API ViewSets
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='api-task')  
router.register(r'admin-logs', AdminLogViewSet, basename='adminlog')  # ✅ Add this line

urlpatterns = [
    # Normal views (HTML pages)
    path('', task_list, name='task-list'),  # Homepage will show tasks
    # path('', task_list, name='home'),  # Homepage will show tasks
    path('add/', add_task, name='add-task'),  # New URL for adding tasks
    path('edit/<int:task_id>/', update_task, name='edit-task'),
    path('delete/<int:task_id>/', delete_task, name='delete-task'),
    path('complete/<int:task_id>/', complete_task, name='complete-task'),
    path("register/", register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="tasks/login.html"), name="login"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # path('api/tasks/', task_list_api, name='task-list-api'),  # New API endpoint GET (List all tasks)
    # path('api/tasks/create/', task_create_api, name='task-create-api'),# New API endpoint  POST (Create a new task)
    # path('api/tasks/<int:task_id>/', task_detail_api, name='task-detail-api'),# New API endpoint GET (Retrieve a single task)
    # path('api/tasks/<int:task_id>/update/', task_update_api, name='task-update-api'),# New API endpoint PUT (Update a task)
    # path('api/tasks/<int:task_id>/delete/', task_delete_api, name='task-delete-api'),# New API endpoint DELETE (Delete a task)
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
    # Include the ViewSet's router
    path('api/', include(router.urls)),  
    
]

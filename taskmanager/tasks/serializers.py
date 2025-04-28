from rest_framework import serializers
from .models import Task  # Import your Task model
from .models import AdminLog
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Task
        fields = '__all__'  # Include all fields in the API response
        # exclude = ['user']  # Exclude `user` from input, since it's set automatically


class AdminLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminLog
        fields = "__all__"
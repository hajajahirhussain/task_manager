from django.contrib import admin

# Register your models here.
from .models import Task
from .models import AdminLog
admin.site.register(Task)

@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ("admin", "action", "task_id", "timestamp")
    search_fields = ("admin__username", "action")
    list_filter = ("timestamp",)

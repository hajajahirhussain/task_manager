from django.contrib import admin

# Register your models here.
from .models import Task
from .models import AdminLog
admin.site.register(Task)

@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ("admin", "action", "task_id", "task_title", "timestamp")
    list_display_links = ("admin", "task_title")
    search_fields = ("admin__username", "action")
    list_filter = ("timestamp",)
    date_hierarchy = "timestamp"

    def task_title(self, obj):
        return obj.task.title
    task_title.short_description = "Task"

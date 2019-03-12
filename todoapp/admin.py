from django.contrib import admin
from todoapp.models import Task, TaskList, Comment,Duration


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task_list","priority","completed", "due_date",)
    list_filter = ("task_list",)
    ordering = ("priority",)
    search_fields = ("name",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "date", "snippet")

class DurationAdmin(admin.ModelAdmin):
    list_display=("user","present_date","in_time","out_time","task_duration",)

admin.site.register(TaskList)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Duration,DurationAdmin)
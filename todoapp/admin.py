from django.contrib import admin
from todoapp.models import Task, TaskList, Comment


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task_list","priority","completed", "due_date",)
    list_filter = ("task_list",)
    ordering = ("priority",)
    search_fields = ("name",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "date", "snippet")

admin.site.register(TaskList)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Task, TaskAdmin)
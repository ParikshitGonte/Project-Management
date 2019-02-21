from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from todoapp.models import Task
from todoapp.utils import staff_check


@login_required
@user_passes_test(staff_check)
def search(request) -> HttpResponse:
    """Search for tasks user has permission to see.
    """
    # queryset_list=Task.objects.active()

    # query = request.GET.get('q') 
    # if query:
    #     queryset_list=queryset_list.filter(
    #         Q(title__icontains=query) | 
    #         Q(note__icontains=query)
    #         ).distinct()


    query_string = ""

    if request.GET:

        found_tasks = None
        if ("q" in request.GET) and request.GET["q"].strip():
            query_string = request.GET["q"]

            found_tasks = Task.objects.filter(
                Q(title__icontains=query_string) | Q(note__icontains=query_string)
            )
        else:
            found_tasks = Task.objects.all()

        if "inc_complete" in request.GET:
            found_tasks = found_tasks.exclude(completed=True)

    else:
        found_tasks = None

    if not request.user.is_superuser:
        found_tasks = found_tasks.filter(task_list__group__in=request.user.groups.all())

    context = {"query_string": query_string, "found_tasks": found_tasks}
    return render(request, "todo/search_results.html", context)
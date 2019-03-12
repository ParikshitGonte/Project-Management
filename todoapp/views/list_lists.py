import datetime
from django.utils import timezone
from operator import mul
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from todoapp.forms import SearchForm,outTimeForm,inTimeForm
from todoapp.models import Task, TaskList,Group,Duration
from todoapp.utils import staff_check


@login_required
@user_passes_test(staff_check)
def list_lists(request) -> HttpResponse:
    """Homepage view - list of lists a user can view, and ability to add a list.
    """

    thedate = datetime.datetime.now()
    searchform = SearchForm(auto_id=False)
    # Make sure user belongs to at least one group.
    if not request.user.groups.all().exists():
        messages.warning(
            request,
            "You do not yet belong to any groups. Ask your administrator to add you to one.",
        )

    # Superusers see all lists
    if request.user.is_superuser:
        lists = TaskList.objects.all().order_by("group", "name")
    else:
        lists = TaskList.objects.filter(group__in=request.user.groups.all()).order_by(
            "group", "name"
        )

    list_count = lists.count()

    # superusers see all lists, so count shouldn't filter by just lists the admin belongs to
    if request.user.is_superuser:
        task_count = Task.objects.filter(completed=0).count()
    else:
        task_count = (
            Task.objects.filter(completed=0)
            .filter(task_list__group__in=request.user.groups.all())
            .count()
        )
    
    form2=outTimeForm()
    form1=inTimeForm()
    if request.method=='POST':
        if 'in_time' in request.POST:
            form1=inTimeForm(request.POST)
            today_min=datetime.datetime.combine(datetime.date.today(),datetime.time.min)
            today_max=datetime.datetime.combine(datetime.date.today(),datetime.time.max)
            duration_instance=Duration.objects.get_or_create(user=request.user,present_date__range=(today_min,today_max))
            duration_instance=Duration.objects.get(user=request.user,present_date__range=(today_min,today_max))
            duration_instance.user = request.user
            duration_instance.save()
           
        elif 'out_time' in request.POST:
            form2=outTimeForm(request.POST)
            today_min=datetime.datetime.combine(datetime.date.today(),datetime.time.min)
            today_max=datetime.datetime.combine(datetime.date.today(),datetime.time.max)
            duration_instance=Duration.objects.get(user=request.user,present_date__range=(today_min,today_max))
            duration_instance.out_time=datetime.datetime.now()
            out_time=duration_instance.out_time.strftime("%H:%M:%S")
            in_time=duration_instance.in_time.strftime("%H:%M:%S")
            fmt="%H:%M:%S"
            difference=datetime.datetime.strptime(out_time,fmt) - datetime.datetime.strptime(in_time,fmt)
            factors=(60,1,1/60)
            out_minutes = sum(map(mul,map(int,out_time.split(':')),factors))
            in_minutes=sum(map(mul,map(int,in_time.split(':')),factors))
            total_minutes=out_minutes-in_minutes
            duration_instance.task_duration=int(total_minutes)
            duration_instance.save()
        else:
            form2=outTimeForm()
            form1=inTimeForm()
    

    

    context = {
        "lists": lists,
        "thedate": thedate,
        "searchform": searchform,
        "list_count": list_count,
        "task_count": task_count,
        "form1":form1,
        "form2":form2,
    }

    return render(request, "todo/list_lists.html", context)

   

    


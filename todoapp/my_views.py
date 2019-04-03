from django.shortcuts import render
from datetime import date
from .forms import userform
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect, render,get_object_or_404
from django.utils.text import slugify
from django.contrib.auth.models import Group, Permission
#from todoapp.forms import AddProjectGroup
from todoapp.utils import staff_check
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from todoapp.models import *

# Create your views here.
@login_required
#@user_passes_test(staff_check)
def add_project_new(request):
    """Allow users to add a new todo list to the group they're in.
    """
    print("\n"*20)
    print("Test1")
    if request.method =='POST':
        new_group = request.POST.get('group_name')
        print("\n"*20)
        print("Test2")
        print(new_group)
        print("\n"*20)

        Group.objects.create(name=new_group)
    return render(request,'todo/add_project.html')

def update_project(request,group_id: int):
    selected_item =Group.objects.get(id=group_id)
    if request.method=='POST':
        update_group=request.POST.get('group_name')
        print(update_group)
        selected_item.name = update_group
        selected_item.save()
        print(Group.objects.get(name=update_group))
        return HttpResponseRedirect('/todoapp')
    return render(request,'todo/update_project.html',{'selected_item':selected_item})

def reports(request):
    status_count=Task.objects.values('status').count()
    inprogress_count=Task.objects.filter(status='INPROGRESS').count()
    complete_count=Task.objects.filter(status='COMPLETE').count()
    verfication_count=Task.objects.filter(status='VERIFICATION').count()
    return render(request,'todo/reports.html',{'status_count':status_count,'inprogress_count':inprogress_count,'complete_count':complete_count,'verfication_count':verfication_count})

def time_reports(request,user_id):
    value=''
    selected_user=User.objects.get(id=user_id)
    myobject=Duration.objects.filter(user=selected_user).order_by('present_date')
    if request.method=='POST':
        form=userform(request.POST)
        if form.is_valid():
            value=request.POST.get("user")
            my_url="/todoapp/time_reports/"+str(value)
            return HttpResponseRedirect(my_url)
    else:
        form=userform()   
    return render(request,'todo/time_reports.html',{'form':form,'myobject':myobject,'value':value})
    # myobject=Duration.objects.all().order_by('present_date').filter(user=request.user)


from django.shortcuts import render
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

    '''
    #form = request.POST
    #if request.method == 'POST':
      selected_item =Group.objects.get(id=group_id)
      name = request.POST.get('group_name')
      selected_item.name = name
      selected_item.name.save()

      return render(request,'todo/update_project.html',{'selected_item':item})

'''
'''
def update_project_form(request, id):
    if request.method == 'POST':
      selected_item = get_object_or_404(Group, id=id)
      name = request.POST.get('group_name')
      selected_item.name = name
      selected_item.save()
    return render(request,'todo/update_project_form.html',{'groups':item})
'''    
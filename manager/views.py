from django.shortcuts import render
from . models import Manager

def manager_list(request):
    managers = Manager.objects.all()
    return render(request,'manager/manager_list.html',{'managers':managers})

def add_manager(request):
    pass
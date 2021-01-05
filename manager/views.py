from django.shortcuts import render,redirect
from . models import Manager
from django.core.paginator import Paginator
from django.contrib.auth.models import User

def manager_list(request):
    if not request.user.is_authenticated:
     return redirect('mylogin')

    
    if request.method == 'POST':
        manager_name = request.POST.get('manager_name')
        if manager_name =='':
            return redirect('manager_list')
        manager =Manager(manager_name= manager_name)
        manager.save()

    managers = Manager.objects.all()
    paginator = Paginator(managers, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'manager/manager_list.html',{'page_obj':page_obj})

def add_user(request):
    if request.method == 'POST':
        user_name= request.POST.get('emp_no')
        first_name = request.POST.get('emp_name')
        email = request.POST.get('emp_email')
    return render(request,'manager/add_user.html')

def users_list(request):
    users = User.objects.all()
    paginator = Paginator(users, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'manager/users_list.html',{'page_obj':page_obj})
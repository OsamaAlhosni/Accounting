from django.shortcuts import render,redirect,get_object_or_404
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

    if not request.user.is_authenticated:
       return redirect('mylogin')

    if request.method == 'POST':
        user_name= request.POST.get('emp_no')
        first_name = request.POST.get('emp_name')
        email = request.POST.get('emp_email')
        password1 = request.POST.get('emp_password1')
        password2 = request.POST.get('emp_password2')
        if user_name == '' or first_name == '' or email == '' or password1 == '' or password2 == '':
            err = 'جميع الحقول إجبارية'
            return render(request,'manager/add_user.html',{'err':err})
        if password1 != password2 :
            err = 'كلمة المرور غير متابطقة'
            return render(request,'manager/add_user.html',{'err':err})
        user = User.objects.create_user(username=user_name,email=email,password=password1,first_name=first_name)
        
        return redirect('users_list')
    else:
        return render(request,'manager/add_user.html')

def users_list(request):

    if not request.user.is_authenticated:
       return redirect('mylogin')

    users = User.objects.all()
    paginator = Paginator(users, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'manager/users_list.html',{'page_obj':page_obj})

def delete_user(request,user_id):

     if not request.user.is_authenticated:
         return redirect('mylogin')

     user = get_object_or_404(User, pk=user_id)
     user.delete()
     return redirect('users_list')

def edit_user(request,user_id):

    if not request.user.is_authenticated:
       return redirect('mylogin')

    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        emp_no = request.POST.get('emp_no')  
        email = request.POST.get('emp_email') 
        emp_name = request.POST.get('emp_name')
        if emp_no == '' or email == '' or emp_name == '':
            err = 'جميع الحقول مطلوبة'
            return render(request,'manager/edit_user.html',{'user':user,'err':err}) 
        user.username=emp_no
        user.first_name= emp_name
        user.email=email
        user.save()
        return redirect('users_list')
    
    return render(request,'manager/edit_user.html',{'user':user})

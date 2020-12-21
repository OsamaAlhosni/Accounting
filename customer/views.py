from django.shortcuts import render,redirect,get_object_or_404
from .models import Customer
from .forms import CustomerForm
from django.core.paginator import Paginator


def customer_list(request):
    customers = Customer.objects.all()
    paginator = Paginator(customers, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'customer/customer_list.html', {'page_obj': page_obj})

def add_customer(request):
  form = CustomerForm()
  if request.method == 'POST':
     form = CustomerForm(request.POST)
     if form.is_valid():
        form.save()
        return redirect('customer_list')
  return render(request, 'customer/add_customer.html', {'form': form})

def edit_customer(request,customer_id):
  customer = get_object_or_404(Customer, pk=customer_id)
  if request.method == 'GET':
        form = CustomerForm(instance=customer)
        return render(request, 'customer/edit_customer.html', {'form': form})
  else:
        try:
            form = CustomerForm(request.POST, instance=customer)
            form.save()
            return redirect('customer_list')
        except:
            return render(request, 'message/msg.html')

def delete_customer(request,customer_id):
  Customer.objects.filter(id=customer_id).delete()
  redirect('customer_list')
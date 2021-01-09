from django.shortcuts import redirect, render, get_object_or_404
from .forms import ReceiptForm
from .models import Receipt

from customer.models import Customer
from django.core.paginator import Paginator


def add_receipt(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')

    customers = Customer.objects.all()

    if request.method == 'POST':
        receipt_no = request.POST.get('receipt_no')
        receipt_date = request.POST.get('receipt_date')
        receipt_amount = request.POST.get('receipt_amount')
        customer_id = request.POST.get('customer_name')
        receipt_notes = request.POST.get('receipt_note')
        receipt_priod = request.POST.get('receipt_priod')
        receipt_year = request.POST.get('receipt_year')
        if receipt_no == "" or receipt_date == "" or receipt_amount == "" or customer_id == "":
            error = 'جميع الحقول إجبارية ويجب إدخالها'
            alert = 'alert-danger'
            url_back = '{% url add_receipt %}'
            context = {
                'error': error,
                'alert': alert,
                'url_back': url_back
            }
            return render(request, 'casa/msg.html', context)
        receipt = Receipt(receipt_no=receipt_no, receipt_date=receipt_date,
                          receipt_amount=receipt_amount, receipt_notes=receipt_notes, customer_id=customer_id, priod=receipt_priod, syear=receipt_year)
        receipt.save()
    return render(request, 'casa/add_receipt.html', {'customers': customers})


def receipt_list(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')

    receipts = Receipt.objects.all()
    paginator = Paginator(receipts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'casa/receipt_list1.html', {'page_obj': page_obj})


def edit_receipt(request, receipt_id):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    receipt = get_object_or_404(Receipt, pk=receipt_id)
    customers = Customer.objects.all()

    if request.method == 'POST':
        receipt_no = request.POST.get('receipt_no')
        receipt_date = request.POST.get('receipt_date')
        receipt_amount = request.POST.get('receipt_amount')
        customer_id = request.POST.get('customer_name')
        receipt_notes = request.POST.get('receipt_note')
        receipt_priod = request.POST.get('receipt_priod')
        receipt_year = request.POST.get('receipt_year')

        if receipt_no == "" or receipt_date == "" or receipt_amount == "" or customer_id == "":
            error = 'جميع الحقول إجبارية ويجب إدخالها'
            alert = 'alert-danger'
            url_back = '{% url add_receipt %}'
            context = {
                'error': error,
                'alert': alert,
                'url_back': url_back
            }
            return render(request, 'casa/msg.html', context)
        receipt.receipt_no = receipt_no
        receipt.receipt_date = receipt_date
        receipt.receipt_amount = receipt_amount
        receipt.receipt_notes = receipt_notes
        receipt.customer_id = customer_id
        receipt.priod= receipt_priod
        receipt.syear = receipt_year
        receipt.save()
        return redirect('receipt_list')
    return render(request, 'casa/edit_receipt.html', {'customers': customers, 'receipt': receipt})


def delete_receipt(request, receipt_id):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    receipt = get_object_or_404(Receipt, pk=receipt_id)
    receipt.delete()
    return redirect('receipt_list')


def msg(request):
    return render(request, 'casa/msg.html')


def casa_search(request):

    return render(request, 'casa/casa_search.html')

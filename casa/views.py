from django.shortcuts import redirect, render, get_object_or_404
from .forms import ReceiptForm
from .models import Receipt, PaymentType, Bank, ReceiptType

from customer.models import Customer
from django.core.paginator import Paginator


def add_receipt(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')

    customers = Customer.objects.all()
    payment_types = PaymentType.objects.all()
    banks = Bank.objects.all()
    receipt_types = ReceiptType.objects.all()

    if request.method == 'POST':
        receipt_no = request.POST.get('receipt_no')
        receipt_date = request.POST.get('receipt_date')
        receipt_amount = request.POST.get('receipt_amount')
        customer_id = request.POST.get('customer_name')
        receipt_notes = request.POST.get('receipt_note')
        receipt_priod = request.POST.get('receipt_priod')
        receipt_year = request.POST.get('receipt_year')
        check_no = request.POST.get('check_no')
        invoice_no = request.POST.get('invoice_no')
        bank_id = request.POST.get('bank_name')
        receipt_type_id = request.POST.get('receipt_type')
        payment_type_id = request.POST.get('payment_type')
        transfare_date = request.POST.get('transfare_date')
        transfare_no = request.POST.get('transfare_no')
        if receipt_no == "" or receipt_date == "" or receipt_amount == "" or customer_id == "" or receipt_priod == "" or receipt_year == "" or receipt_type_id == "" or bank_id == "":
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
                          receipt_amount=receipt_amount, receipt_notes=receipt_notes, customer_id=customer_id, priod=receipt_priod,
                          syear=receipt_year, check_no=check_no, invoice_no=invoice_no, bank_id=bank_id, receipt_type_id=receipt_type_id,
                          payment_type_id=payment_type_id,  transfare_no=transfare_no)
        receipt.save()
        print(bank_id)
    context = {
        'customers': customers,
        'payment_types': payment_types,
        'banks': banks,
        'receipt_types': receipt_types,
    }
    return render(request, 'casa/add_receipt.html', context)


def receipt_list(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    customers = Customer.objects.all()
    year_search = Receipt.objects.values_list('syear',flat=True).distinct()
    invoices = Receipt.objects.filter()


    receipts = Receipt.objects.all()
    paginator = Paginator(receipts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'customers':customers,
        'year_search':year_search,
        }

    return render(request, 'casa/receipt_list1.html', context)


def edit_receipt(request, receipt_id):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    receipt = get_object_or_404(Receipt, pk=receipt_id)
    customers = Customer.objects.all()
    payment_types = PaymentType.objects.all()
    banks = Bank.objects.all()
    receipt_types = ReceiptType.objects.all()

    if request.method == 'POST':
        receipt_no = request.POST.get('receipt_no')
        receipt_date = request.POST.get('receipt_date')
        receipt_amount = request.POST.get('receipt_amount')
        customer_id = request.POST.get('customer_name')
        receipt_notes = request.POST.get('receipt_note')
        receipt_priod = request.POST.get('receipt_priod')
        receipt_year = request.POST.get('receipt_year')
        check_no = request.POST.get('check_no')
        invoice_no = request.POST.get('invoice_no')
        bank_id = request.POST.get('bank_name')
        receipt_type_id = request.POST.get('receipt_type')
        payment_type_id = request.POST.get('payment_type')
        transfare_date = request.POST.get('transfare_date')
        transfare_no = request.POST.get('transfare_no')

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
        receipt.priod = receipt_priod
        receipt.syear = receipt_year
        receipt.check_no = check_no
        receipt.invoice_no = invoice_no
        receipt.bank_id = bank_id
        receipt.receipt_type_id = receipt_type_id
        receipt.payment_type_id = payment_type_id
        # if  transfare_date :
        #     receipt.transfare_date = transfare_date
        receipt.transfare_no = transfare_no

        receipt.save()
        return redirect('receipt_list')
    else:
        context = {
            'customers': customers,
            'payment_types': payment_types,
            'banks': banks,
            'receipt_types': receipt_types,
            'receipt': receipt,
        }
        return render(request, 'casa/edit_receipt.html', context)


def delete_receipt(request, receipt_id):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    receipt = get_object_or_404(Receipt, pk=receipt_id)
    receipt.delete()
    return redirect('receipt_list')


def msg(request):
    return render(request, 'casa/msg.html')


def casa_search(request):
    total_receipt =0
    receipts = Receipt.objects.all()
    receipt_no = request.POST.get('receipt_no')
    priod = request.POST.get('priod')
    customer_name= request.POST.get('customer_name')
    year = request.POST.get('year')
    if receipt_no != '':
        receipts = receipts.filter(receipt_no = receipt_no)

    if int(customer_name) > 0:
      receipts = receipts.filter(customer_id = customer_name)  

    if int(priod) > 0:
      receipts = receipts.filter(priod = priod)  

    if year != '0':
        receipts = receipts.filter(syear = year)  
    for i in receipts:
        total_receipt +=  i.receipt_amount
    paginator = Paginator(receipts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'receipts':page_obj,
        'total_receipt':total_receipt,
    }

    return render(request, 'casa/casa_search.html',context)

def receipt_detail(request,receipt_id):
    receipt = get_object_or_404(Receipt, pk=receipt_id)
    context = {
        'receipt':receipt,
    }
    return render(request,'casa/receipt_detail.html',context)

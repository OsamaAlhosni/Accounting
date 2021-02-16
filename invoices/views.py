from django.shortcuts import redirect, render, get_object_or_404
from .models import Invoice,Customer
from django.http import HttpResponseRedirect
from django.contrib import messages
from tablib import Dataset
from django.core.paginator import Paginator
import decimal
from datetime import datetime
from django.utils.formats import get_format
from .forms import InvoiceForm

def parse_date(date_str):
    """Parse date from string by DATE_INPUT_FORMATS of current language"""
    for item in get_format('DATE_INPUT_FORMATS'):
        try:
            return datetime.strptime(date_str, item).date()
        except (ValueError, TypeError):
            continue

    return None


def upload_invoice(request):

    if not request.user.is_authenticated:
     return redirect('mylogin')

    if request.method == 'POST':
        dataset = Dataset()
        new_invoice = request.FILES["myfile"]
        if not new_invoice.name.endswith('xlsx'):
            messages.info(request, 'wrong file')
            return render(request, 'invoice/upload_invoice.html')
        imported_data = dataset.load(new_invoice.read(), format='xlsx')
        for data in imported_data:
            customer_id = data[0]
            customer_name = data[1]
            balance = data[2]
            if balance is None:
                balance = 0.0
            balance = decimal.Decimal(balance)
            from_date = data[3]
            balance_to = data[4]
            proid = data[5]
            year = data[6]
            Invoice_no = data[7]
            invoice_amount = data[8]
            if invoice_amount is None:
                invoice_amount = 0.0
            invoice_amount = decimal.Decimal(invoice_amount)
            notes = data[9]
            
            try:
                find_customer = Customer.objects.get(pk=customer_id)
            # except Customer.DoesNotExist:
            except Exception as e:
                print(type(e),customer_id)
                find_customer =  Customer.objects.get(pk=1)
            try:
                Invoice.objects.create(
                    customer_id=find_customer, customer_name=customer_name, from_date=from_date, balance_to=balance_to, proid=proid, tyear=year, Invoice_no=Invoice_no, invoice_amount=invoice_amount, notes=notes, balance=balance)

            except TypeError as e:
                print(e)
    invoices = Invoice.objects.filter(commited=False)
    context = {
        'invoices': invoices
    }

    paginator = Paginator(invoices, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'invoice/upload_invoice.html', {'page_obj': page_obj})


def invoice_list(request):

    if not request.user.is_authenticated:
     return redirect('mylogin')
    customers = Customer.objects.all()
    year_search = Invoice.objects.values_list('tyear',flat=True).distinct()
    invoices = Invoice.objects.filter(commited=True)

    paginator = Paginator(invoices, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': invoices,
        'customers':customers,
        'year_search':year_search,
        }
    return render(request, 'invoice/invoice_list1.html', context)


def edit_invoice(request, invoice_id):

    if not request.user.is_authenticated:
     return redirect('mylogin')

    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        balance = request.POST.get('balance')
        invoice_no = request.POST.get('invoice_no')
        invoice_amount = request.POST.get('invoice_amount')
        fromdate = request.POST.get('ff')
        fdate = parse_date(fromdate)
        balance_to = request.POST.get('tt')
        tdate = parse_date(balance_to)
        notes = request.POST.get('notes')
        invoice.customer_name = customer_name
        invoice.balance = balance
        invoice.Invoice_no = invoice_no
        invoice.invoice_amount = invoice_amount
        invoice.from_date = fdate
        invoice.balance_to = tdate
        invoice.notes = notes
        invoice.save()
        message = 'تمت عملية الحفظ بنجاح'
        return render(request,'invoice/edit_invoice.html',{'invoice': invoice,'message':message})
        
    return render(request, 'invoice/edit_invoice.html', {'invoice': invoice})


def save_to_database(request):

    if not request.user.is_authenticated:
     return redirect('mylogin')

    update_counts = Invoice.objects.filter(
        commited=False).update(commited=True)
    return redirect('invoice_list')


def delete_invoice(request, invoice_id):

    if not request.user.is_authenticated:
     return redirect('mylogin')

    invoice = get_object_or_404(Invoice, pk=invoice_id)
    invoice.delete()
    return redirect('invoice_list')

def search(request):
    invoices = Invoice.objects.all()
    invoice_no = request.POST.get('invoice_no')
    priod = request.POST.get('priod')
    customer_name= request.POST.get('customer_name')
    year = request.POST.get('year')

    if invoice_no != '':
        invoices = invoices.filter(Invoice_no = invoice_no)

    if int(customer_name) > 0:
      invoices = invoices.filter(customer_id_id = customer_name)  

    if int(priod) > 0:
      invoices = invoices.filter(proid = priod)  

    if year != '0':
        invoices = invoices.filter(tyear = year)  

    paginator = Paginator(invoices, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'invoices':page_obj
    }

    return render(request,'invoice/search.html',context)

def invoice_detail(request,invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    context = {
        'invoice':invoice,
    }
    return render(request,'invoice/invoice_detail.html',context)

def create_invoice(request):
    form = InvoiceForm(request.POST)
    if request.method == 'POST':
      
        if form.is_valid:
            print('ssss')
            form.save()
            return redirect('invoice_list')

    context = {
        'form':form,
    }
    
    return render(request,'invoice/invoice_form.html',context)
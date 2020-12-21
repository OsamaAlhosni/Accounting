from django.shortcuts import render
from invoices.models import Invoice
from casa.models import Receipt
from customer import Customer
from django.db.models import Count, Sum

from django.contrib.humanize.templatetags.humanize import intcomma


def index(request):

    # Invoice Chart label & data
    labels = []
    data = []

    # Receipt Chart label & data
    rlabels = []
    rdata = []

    # All customer count
    all_customer = Invoice.objects.values_list(
        'customer_name').order_by('customer_name').distinct().count()

    # Total All Receipts
    all_receipt_amount = Receipt.objects.aggregate(
        sum=Sum('receipt_amount')).get('sum')
    if all_receipt_amount:
        all_receipt_amount = f"د.ل {intcomma('{:0.3f}'.format(all_receipt_amount))}"
    else:
        all_receipt_amount = 0        

    # Total All invoices
    all_invoice_amount = Invoice.objects.aggregate(
        sum=Sum('invoice_amount')).get('sum')
    if all_invoice_amount:
        all_invoice_amount = f"{intcomma('{:0.3f}'.format(all_invoice_amount))} د.ل "
    else:
        all_invoice_amount = 0

    # Total Invoice used in Chart
    queryset = Invoice.objects.filter(invoice_amount__gt= 0).values('customer_name').annotate(
        total_sales=Sum('invoice_amount')).order_by('customer_name')[:5]
    for entry in queryset:
        labels.append(entry['customer_name'])
        data.append(float(entry['total_sales']))

    # Total Receipts used in Charts
    queryset = Receipt.objects.filter(receipt_amount__gt= 0).values('customer').annotate(
        total_receipt=Sum('receipt_amount')).order_by('customer')[:5]
    for entry in queryset:
       customer_name = Customer.objects.filter(id=entry['customer']) 
       rlabels.append(customer_name)
       rdata.append(float(entry['total_receipt']))
   
    context = {
        'all_customer': all_customer,
        'all_invoice_amount': all_invoice_amount,
        'all_receipt_amount': all_receipt_amount,
        'labels': labels,
        'data': data,
        'rlabels': rlabels,
        'rdata': rdata,
    }
    
    return render(request, 'accountdash/index.html', context)

def index2(request):
    return render(request,'ticket/index2.html')

def ticket_list(request):
    return render(request,'ticket/ticket.html')
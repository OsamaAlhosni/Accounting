from django.shortcuts import render, redirect
from invoices.models import Invoice
from casa.models import Receipt
from customer.models import Customer, CustomerCatogry
from django.db.models import Sum, Max
from django.contrib.auth import authenticate,login,logout
from django.contrib.humanize.templatetags.humanize import intcomma


def index(request):

        if not request.user.is_authenticated:
            return redirect('mylogin')


        # Invoice Chart label & data
        labels = []
        data = []

        # Receipt Chart label & data
        rlabels = []
        rdata = []

        # Total Invoice By Catagory
        cat_label = []
        cat_data = []

        # Total Invoices & payment
        total_invoice_label = []
        total_invoice_date = []
        total_payment_label = []
        total_payment_data = []
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
        queryset = Invoice.objects.filter(invoice_amount__gt=0).values('customer_name').annotate(
            total_sales=Sum('invoice_amount')).order_by('-total_sales')[:5]

        for entry in queryset:
            labels.append(entry['customer_name'])
            data.append(float(entry['total_sales']))

        # Total Receipts used in Charts
        queryset = Receipt.objects.filter(receipt_amount__gt=0).values('customer').annotate(
            total_receipt=Sum('receipt_amount')).order_by('customer')[:5]
        for entry in queryset:
            customer = Customer.objects.get(id=entry['customer'])
            rlabels.append(customer.customer_name)
            rdata.append(float(entry['total_receipt']))

        # Total Invoices By Customer Catagory
        queryset = Invoice.objects.values('customer_id__customer_cat__type_desc').annotate(
            total_sales=Sum('invoice_amount')).order_by('-total_sales')[:5]
        for entry in queryset:
            cat_label.append(entry['customer_id__customer_cat__type_desc'])
            cat_data.append(float(entry['total_sales']))

        # Total Sales & Receipts

        invoices = Invoice.objects.all()[:5]
        for invoice in invoices:
            i_total = Invoice.objects.annotate(total_sales=Sum('invoice_amount')).filter(customer_id_id =invoice.customer_id_id)
            r_total = Receipt.objects.annotate( total_receipt=Sum('receipt_amount')).filter(customer_id = invoice.customer_id_id)
            if r_total :
                for j in r_total:
                    total_payment_data.append(float(j.total_receipt))
            else:
                total_payment_label.append(float(0))
                
            for i in i_total:
                total_invoice_label.append(i.customer_name)
                total_invoice_date.append(float(i.total_sales))

        context = {
            'all_customer': all_customer,
            'all_invoice_amount': all_invoice_amount,
            'all_receipt_amount': all_receipt_amount,
            'labels': labels,
            'data': data,
            'rlabels': rlabels,
            'rdata': rdata,
            'cat_label': cat_label,
            'cat_data': cat_data,
            'total_invoice': total_invoice_date,
            'total_receipt': total_payment_data,
            'total_invoice_label': total_invoice_label,
        }

        return render(request, 'accountdash/index.html', context)


def index2(request):
    if not request.user.is_authenticated:
     return redirect('mylogin')

    return render(request, 'ticket/index2.html')


def ticket_list(request):
    if not request.user.is_authenticated:
     return redirect('mylogin')

    return render(request, 'ticket/ticket.html')

def sales_report(request):
    if not request.user.is_authenticated:
     return redirect('mylogin')

    return render(request,'accountdash/sales_report.html')

def mylogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username != '' and password != '':
            user = authenticate(username=username,password=password)

            if user != None:
                login(request,user)
                return redirect('index')
            else:
                err = 'خطأ في اسم المستخدم أو كلمة المرور'
                return render(request,'accountdash/login.html',{'err':err})            
        
    return render(request,'accountdash/login.html')

def mylogout(request):
    logout(request)
    return redirect('mylogin')
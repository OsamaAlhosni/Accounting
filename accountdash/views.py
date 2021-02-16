from django.shortcuts import render, redirect
from invoices.models import Invoice
from casa.models import Receipt
from customer.models import Customer, CustomerCatogry
from django.contrib.auth.models import User
from django.db.models import Sum, Max
from django.contrib.auth import authenticate, login, logout
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth.decorators import login_required


@login_required(login_url='/mylogin')
def index(request):

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
    all_customer = Customer.objects.count()

    # Total All Receipts
    all_receipt_amount = Receipt.objects.aggregate(
        sum=Sum('receipt_amount')).get('sum')
    print(all_receipt_amount)
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
    queryset = Invoice.objects.select_related('account_customer').all() \
        .values('customer_id_id') \
        .annotate(total_sales=Sum('invoice_amount')) \
        .order_by('-total_sales')[:5]

    for entry in queryset:
        customer = Customer.objects.get(id=entry['customer_id_id'])
        labels.append(customer.customer_name)
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
        total_sales=Sum('invoice_amount')).order_by('-total_sales')
    for entry in queryset:
        cat_label.append(entry['customer_id__customer_cat__type_desc'])
        cat_data.append(float(entry['total_sales']))

    # Total Sales & Receipts

    squeryset = Invoice.objects.filter(invoice_amount__gt=0).values('customer_id_id').annotate(
        total_sales=Sum('invoice_amount'))[:20]
    for i in squeryset:
        cust = Customer.objects.get(id=i['customer_id_id'])
        total_invoice_label.append(cust.customer_name)
        rqueryset = Receipt.objects.filter(receipt_amount__gt=0).values('customer').annotate(
            total_receipt=Sum('receipt_amount')).filter(customer_id__customer_name=cust.customer_name)
        for j in rqueryset:
            if (j['total_receipt']):
                total_payment_data.append(float(j['total_receipt']))
            else:
                total_payment_data.append(float(0))

        total_invoice_date.append(float(i['total_sales']))
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


@login_required(login_url='/mylogin')
def index2(request):

    return render(request, 'ticket/index2.html')


@login_required(login_url='/mylogin')
def ticket_list(request):

    return render(request, 'ticket/ticket.html')


@login_required(login_url='/mylogin')
def sales_report(request):
    # Invoice Chart label & data
    labels = []
    data = []
    prepare = []
    percent = []
    total_sales = 0
    customer_cat = CustomerCatogry.objects.all()

    if request.method == 'POST':
        priod = request.POST.get('priod')
        cat = request.POST.get('cat')
        customer_list = Customer.objects.filter(customer_cat_id=cat)
        year = request.POST.get('year')
        if year and int(priod) > 0:
            queryset = Invoice.objects.select_related('account_customer').all() \
                .values('customer_id_id') \
                .annotate(total_sales=Sum('invoice_amount')) \
                .filter(customer_id__customer_cat__id=cat, tyear=year, proid=priod)
        else:
            queryset = Invoice.objects.select_related('account_customer').all() \
                .values('customer_id_id') \
                .annotate(total_sales=Sum('invoice_amount')) \
                .filter(customer_id__customer_cat__id=cat)
        for entry in queryset:
            cust = Customer.objects.get(id=entry['customer_id_id'])
            labels.append(cust.customer_name)
            data.append(float(entry['total_sales']))
            total_sales += float(entry['total_sales'])
            prepare.append({'customer_id': cust.pk, 'customer_name': cust.customer_name,
                            'total_sales': float(entry['total_sales'])})
        percet_sales = total_sales
        for i in prepare:
            net_percent = round((i['total_sales']/percet_sales)*100, 2)
            s = f"{intcomma('{:0.3f}'.format(i['total_sales']))} د.ل "
            percent.append(
                {'customer_id': i['customer_id'], 'customer_name': i['customer_name'], 'net_percent': net_percent, 'total_sales': s})

        total_sales = f"{intcomma('{:0.3f}'.format(total_sales))} د.ل "

        context = {
            'customer_cat': customer_cat,
            'data': data,
            'labels': labels,
            'year': year,
            'priod': int(priod),
            'cat_set': int(cat),
            'total_sales': total_sales,
            'customer_list': customer_list,
            'percet_sales': percet_sales,
            'percent': percent
        }
        return render(request, 'accountdash/sales_report.html', context)
    return render(request, 'accountdash/sales_report.html', {'customer_cat': customer_cat})


def receipt_report(request):

    # Receipts Detail Chart label & data
    labels = []
    data = []
    prepare = []
    percent = []

    total_receipt = 0
    customer_cat = CustomerCatogry.objects.all()

    if request.method == 'POST':
        priod = request.POST.get('priod')
        cat = request.POST.get('cat')
        year = request.POST.get('year')
        if year and int(priod) > 0:
            queryset = Receipt.objects.filter(receipt_amount__gt=0).values('customer').annotate(
                total_receipt=Sum('receipt_amount')).filter(customer_id__customer_cat__id=cat, priod=priod, syear=year)
        elif not year and int(priod) > 0:
            queryset = Receipt.objects.filter(receipt_amount__gt=0).values('customer').annotate(
                total_receipt=Sum('receipt_amount')).filter(customer_id__customer_cat__id=cat, priod=priod)
        else:
            queryset = Receipt.objects.filter(receipt_amount__gt=0).values('customer').annotate(
                total_receipt=Sum('receipt_amount')).filter(customer_id__customer_cat__id=cat)

        for entry in queryset:
            customer = Customer.objects.get(id=entry['customer'])
            labels.append(customer.customer_name)
            data.append(float(entry['total_receipt']))
            total_receipt += float(entry['total_receipt'])
            prepare.append({'customer_id': customer.pk, 'customer_name': customer.customer_name,
                            'total_receipt': float(entry['total_receipt'])})
        percet_sales = total_receipt
        for i in prepare:
            net_percent = round((i['total_receipt']/percet_sales)*100, 2)
            s = f"{intcomma('{:0.3f}'.format(i['total_receipt']))} د.ل "
            percent.append(
                {'customer_id': i['customer_id'], 'customer_name': i['customer_name'], 'net_percent': net_percent, 'total_receipt': s})
        

        total_receipt = f"{intcomma('{:0.3f}'.format(total_receipt))} د.ل "
        context = {
            'customer_cat': customer_cat,
            'data': data,
            'labels': labels,
            'year': year,
            'priod': int(priod),
            'cat_set': int(cat),
            'total_receipt': total_receipt,
            'percet_sales': percet_sales,
            'percent': percent,
        }

        return render(request, 'accountdash/receipt_report.html', context)
    return render(request, 'accountdash/receipt_report.html', {'customer_cat': customer_cat})


def total_inv_rec_report(request):
    ilabels = []
    idata = []
    rlabel = []
    rdata = []
    customer_blance = []
    receipts = 0
    total_receipt = 0
    total_sales = 0
    customer_cat = CustomerCatogry.objects.all()
    if request.method == 'POST':
        priod = request.POST.get('priod')
        cat = request.POST.get('cat')
        year = request.POST.get('year')
        print(year)
        if year and int(priod) > 0:
            iqueryset = Invoice.objects.filter(invoice_amount__gt=0).values('customer_id_id').annotate(
                total_sales=Sum('invoice_amount')).filter(customer_id__customer_cat__id=cat, proid=priod, tyear=year)
        elif not year and int(priod) > 0:
            iqueryset = Invoice.objects.filter(invoice_amount__gt=0).values('customer_id_id').annotate(
                total_sales=Sum('invoice_amount')).filter(customer_id__customer_cat__id=cat, proid=priod)
        else:
            iqueryset = Invoice.objects.filter(invoice_amount__gt=0).values('customer_id_id').annotate(
                total_sales=Sum('invoice_amount')).filter(customer_id__customer_cat__id=cat)

        for i in iqueryset:
            receipts = 0
            c_balance = 0
            cust = Customer.objects.get(id=i['customer_id_id'])
            ilabels.append(cust.customer_name)

            if year and int(priod) > 0:
                rqueryset = Receipt.objects.filter(receipt_amount__gt=0, customer_id__customer_name=cust.customer_name, priod=priod, syear=year).values('customer_id').annotate(
                    total_receipt=Sum('receipt_amount'))
            elif not year and int(priod) > 0:
                rqueryset = Receipt.objects.filter(receipt_amount__gt=0, customer_id__customer_name=cust.customer_name, priod=priod).values('customer_id').annotate(
                    total_receipt=Sum('receipt_amount'))
            else:
                rqueryset = Receipt.objects.filter(receipt_amount__gt=0, customer_id__customer_name=cust.customer_name).values('customer_id').annotate(
                    total_receipt=Sum('receipt_amount'))

            for j in rqueryset:

                if (j['total_receipt']):
                    receipts = float(j['total_receipt'])
                    rdata.append(float(j['total_receipt']))
                    total_receipt += float(j['total_receipt'])
                else:
                    receipts = 0
                    rdata.append(float(0))
            c_balance = receipts - float(i['total_sales'])
            customer_blance.append({'customer_id': i['customer_id_id'], 'customer_name': cust.customer_name,
                                    'total_invoice': f"{intcomma('{:0.3f}'.format(float(i['total_sales'])))} د.ل ",
                                    'total_receipt': f"{intcomma('{:0.3f}'.format(receipts))} د.ل ",
                                    'c_balance': f"{intcomma('{:0.3f}'.format( c_balance)) } د.ل ", })
            idata.append(float(i['total_sales']))
            total_sales += float(i['total_sales'])

        balance = total_sales - total_receipt
        flag = False
        if balance < 0:
            flag = True
        else:
            flag = False

        total_receipt = f"{intcomma('{:0.3f}'.format(total_receipt))} د.ل "
        total_sales = f"{intcomma('{:0.3f}'.format(total_sales))} د.ل "
        balance = f"{intcomma('{:0.3f}'.format(balance))} د.ل "
        context = {
            'ilabels': ilabels,
            'idata': idata,
            'rlabel': rlabel,
            'rdata': rdata,
            'customer_cat': customer_cat,
            'year': year,
            'priod': int(priod),
            'cat_set': int(cat),
            'total_sales': total_sales,
            'total_receipt': total_receipt,
            'balance': balance,
            'customer_blance': customer_blance,
            'flag': flag,
        }
        return render(request, 'accountdash/total_invoice_receipt_report.html', context)

    return render(request, 'accountdash/total_invoice_receipt_report.html', {'customer_cat': customer_cat})


def mylogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username != '' and password != '':
            user = authenticate(username=username, password=password)

            if user != None:
                login(request, user)
                return redirect('index')
            else:
                err = 'خطأ في اسم المستخدم أو كلمة المرور'
                return render(request, 'accountdash/login.html', {'err': err})
    return render(request, 'accountdash/login.html')


def mylogout(request):
    logout(request)
    return redirect('mylogin')


def change_password(request):
    if request.method == 'POST':
        oldpassword = request.POST.get('old_password')
        newpassword1 = request.POST.get('password1')
        newpassword2 = request.POST.get('password2')
        if oldpassword == '' or newpassword1 == '' or newpassword2 == '':
            err = 'جميع الحقول إجبارية'
            return render(request, 'accountdash/change_password.html', {'err': err})
        else:
            if newpassword1 != newpassword2:
                err = 'كلمة المرور غير متطابقة. يرجى إعادة الإدخال'
                return render(request, 'accountdash/change_password.html', {'err': err})
            else:
                user = authenticate(username=request.user,
                                    password=oldpassword)
                if user != None:
                    user = User.objects.get(username=request.user)
                    user.set_password(newpassword1)
                    user.save()
                    logout(request)
                    return redirect('mylogin')
                else:
                    err = 'كلمة المرور القديمة غير صحيحة.. يرجى إعادة الإدخال'
                    return render(request, 'accountdash/change_password.html', {'err': err})
    return render(request, 'accountdash/change_password.html')


def customer_invoice(request, customer_id, priod):
    total = 0
    if priod == 0:
        customer_invoices = Invoice.objects.filter(
            invoice_amount__gt=0, customer_id_id=customer_id)
    else:
        customer_invoices = Invoice.objects.filter(
            invoice_amount__gt=0, customer_id_id=customer_id, proid=priod)
    cust = Customer.objects.get(id=customer_id)
    for i in customer_invoices:
        total += i.invoice_amount
    context = {
        'cust': cust,
        'customer_invoices': customer_invoices,
        'total': total,
    }

    return render(request, 'accountdash/customer_invoice.html', context)

def customer_receipt(request,customer_id, priod):
    total = 0
    if priod == 0:
        customer_receipts = Receipt.objects.filter(
            receipt_amount__gt=0, customer_id=customer_id)
    else:
        customer_receipts = Receipt.objects.filter(
            receipt_amount__gt=0, customer_id=customer_id, priod=priod)
    cust = Customer.objects.get(id=customer_id)
    for i in customer_receipts:
        total += i.receipt_amount
    context = {
        'cust': cust,
        'customer_receipts': customer_receipts,
        'total': total,
    }

    return render(request, 'accountdash/customer_receipt.html', context)


def customer_balance(request,customer_id,priod,year):
    total_invoice=0
    total_receipt = 0
    transaction = []
    balance = 0
    
    customer_invoices = Invoice.objects.filter(
            invoice_amount__gt=0, customer_id_id=customer_id)
    if priod != 0:            
        print(priod)
        customer_invoices = customer_invoices.filter(proid=priod)
    if year != 0:
       
        customer_invoices = customer_invoices.filter(tyear=year)
    cust = Customer.objects.get(id=customer_id)

    for i in customer_invoices:
        customer_receipt = Receipt.objects.filter(customer_id=i.customer_id_id,priod = i.proid)
        
        if customer_receipt:
            for j in customer_receipt:
                transaction.append({'customer_id':i.customer_id_id,'customer_name':cust.customer_name,'invoice_no':i.Invoice_no,
                'invoice_amount':i.invoice_amount,'receipt_no':j.receipt_no,'receipt_amount':j.receipt_amount,'priod':i.proid,'year':i.tyear,'invoice_id':i.id,})
                total_receipt += j.receipt_amount
        else:
            transaction.append({'customer_id':i.customer_id_id,'customer_name':cust.customer_name,'invoice_no':i.Invoice_no,
             'invoice_amount':i.invoice_amount,'receipt_no':'','receipt_amount':'','priod':i.proid,'year':i.tyear,'invoice_id':i.id,})
        total_invoice += i.invoice_amount
    balance = total_invoice - total_receipt
    if balance < 0:
        flag =True
    else:
        flag = False
    balance = f"{intcomma('{:0.3f}'.format(balance))} د.ل "   
    context = {
        'cust': cust,
        'total_invoice': f"{intcomma('{:0.3f}'.format(total_invoice))} د.ل ",
        'total_receipt':f"{intcomma('{:0.3f}'.format(total_receipt))} د.ل ",
        'transaction':transaction,
        'balance': balance,
        'flag':flag,
    }

    return render(request,'accountdash/customer_balance.html',context)
from django.shortcuts import render, redirect
from invoices.models import Invoice
from casa.models import Receipt
from customer.models import Customer, CustomerCatogry
from django.contrib.auth.models import User
from django.db.models import Sum, Max
from django.contrib.auth import authenticate,login,logout
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
        queryset=Invoice.objects.select_related('account_customer').all() \
            .values('customer_id_id' ) \
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
        iqueryset = Invoice.objects.filter(invoice_amount__gt=0).values('customer_name').annotate(
                total_sales=Sum('invoice_amount'))[:10]
        for i in iqueryset:
            total_invoice_label.append(i['customer_name'])
            rqueryset = Receipt.objects.filter(receipt_amount__gt=0).values('customer').annotate(
                total_receipt=Sum('receipt_amount')).filter(customer_id__customer_name=i['customer_name'])
            for j in rqueryset:
                if (j['total_receipt']):
                    total_payment_data.append(float(j['total_receipt']))
                else:
                    total_payment_data.append(float(0))
            print(rqueryset,i['customer_name'])    
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
    total_sales =0
    customer_cat = CustomerCatogry.objects.all()

    if request.method == 'POST':
        priod = request.POST.get('priod')
        cat= request.POST.get('cat')
        year = request.POST.get('year')
        if  year and int(priod) > 0 :
            queryset=Invoice.objects.select_related('account_customer').all() \
            .values('customer_id_id' ) \
            .annotate(total_sales=Sum('invoice_amount')) \
            .filter(customer_id__customer_cat__id =cat,tyear=year,proid=priod)
        else:               
            queryset=Invoice.objects.select_related('account_customer').all() \
            .values('customer_id_id' ) \
            .annotate(total_sales=Sum('invoice_amount')) \
            .filter(customer_id__customer_cat__id =cat)
        for entry in queryset:
            cust= Customer.objects.get(id =entry['customer_id_id'] )            
            labels.append(cust.customer_name)
            data.append(float(entry['total_sales']))
            total_sales += float(entry['total_sales'])
        total_sales = f"{intcomma('{:0.3f}'.format(total_sales))} د.ل "
        context = {
        'customer_cat':customer_cat,
        'data':data,
        'labels':labels,
        'year':year,
        'priod':int(priod),
        'cat_set':int(cat),
        'total_sales':total_sales,
         }  
        return render(request,'accountdash/sales_report.html',context)
    return render(request,'accountdash/sales_report.html',{'customer_cat':customer_cat})

def receipt_report(request):

    # Receipts Detail Chart label & data
    labels = []
    data = []
    total_receipt = 0
    customer_cat = CustomerCatogry.objects.all()

    if request.method == 'POST':
        priod = request.POST.get('priod')
        cat= request.POST.get('cat')
        year = request.POST.get('year')
        if year and int(priod) > 0 :
            queryset = Receipt.objects.filter(receipt_amount__gt=0).values('customer').annotate(
            total_receipt=Sum('receipt_amount')).filter(customer_id__customer_cat__id =cat,priod=priod,syear=year)
        elif not year and int(priod) > 0:
            queryset = Receipt.objects.filter(receipt_amount__gt=0).values('customer').annotate(
            total_receipt=Sum('receipt_amount')).filter(customer_id__customer_cat__id =cat,priod=priod)
        else:
            queryset = Receipt.objects.filter(receipt_amount__gt=0).values('customer').annotate(
            total_receipt=Sum('receipt_amount')).filter(customer_id__customer_cat__id =cat)

        for entry in queryset:
            customer = Customer.objects.get(id=entry['customer'])
            labels.append(customer.customer_name)
            data.append(float(entry['total_receipt']))
            total_receipt += float(entry['total_receipt'])
        total_receipt = f"{intcomma('{:0.3f}'.format(total_receipt))} د.ل "
        context = {
        'customer_cat':customer_cat,
        'data':data,
        'labels':labels,
        'year':year,
        'priod':int(priod),
        'cat_set':int(cat),
        'total_receipt':total_receipt,
         }  

        return render(request,'accountdash/receipt_report.html',context)
    return render(request,'accountdash/receipt_report.html',{'customer_cat':customer_cat})

def total_inv_rec_report(request):
    ilabels = []
    idata = []
    rlabel = []
    rdata = []
    total_receipt = 0
    total_sales = 0
    customer_cat = CustomerCatogry.objects.all()
    if request.method == 'POST':
        priod = request.POST.get('priod')
        cat= request.POST.get('cat')
        year = request.POST.get('year')

        if year and int(priod) > 0 :
            iqueryset = Invoice.objects.filter(invoice_amount__gt=0).values('customer_name').annotate(
                total_sales=Sum('invoice_amount')).filter(customer_id__customer_cat__id =cat,proid=priod,syear=year)
        elif not year and int(priod) > 0:  
            iqueryset = Invoice.objects.filter(invoice_amount__gt=0).values('customer_name').annotate(
                total_sales=Sum('invoice_amount')).filter(customer_id__customer_cat__id =cat,proid=priod)
        else:
            iqueryset = Invoice.objects.filter(invoice_amount__gt=0).values('customer_name').annotate(
                total_sales=Sum('invoice_amount')).filter(customer_id__customer_cat__id =cat)

        for i in iqueryset:
            ilabels.append(i['customer_name'])
            rqueryset = Receipt.objects.filter(receipt_amount__gt=0).values('customer').annotate(
                total_receipt=Sum('receipt_amount')).filter(customer_id__customer_name=i['customer_name'])
            for j in rqueryset:
                if (j['total_receipt']):
                    rdata.append(float(j['total_receipt']))
                    total_receipt += float(j['total_receipt'])
                else:
                    rdata.append(float(0))
            idata.append(float(i['total_sales']))
            total_sales += float(i['total_sales'])
        balance = total_sales - total_receipt    
        total_receipt = f"{intcomma('{:0.3f}'.format(total_receipt))} د.ل "
        total_sales = f"{intcomma('{:0.3f}'.format(total_sales))} د.ل "
        balance = f"{intcomma('{:0.3f}'.format(total_sales))} د.ل "
        context = {
                'ilabels':ilabels,
                'idata':idata,
                'rlabel':rlabel,
                'rdata':rdata,
                'customer_cat':customer_cat,
                'year':year,
                'priod':int(priod),
                'cat_set':int(cat),   
                'total_sales': total_sales,
                'total_receipt': total_receipt,             
                'balance': balance,
            }
        return render(request,'accountdash/total_invoice_receipt_report.html',context)
        
    return render(request,'accountdash/total_invoice_receipt_report.html',{'customer_cat':customer_cat})

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

def change_password(request):
    if request.method == 'POST':
        oldpassword = request.POST.get('old_password')
        newpassword1 = request.POST.get('password1')
        newpassword2=request.POST.get('password2')
        if oldpassword == '' or newpassword1 == '' or newpassword2 == '':
            err= 'جميع الحقول إجبارية'
            return render(request,'accountdash/change_password.html',{'err':err})
        else:
            if newpassword1 != newpassword2 :
                err = 'كلمة المرور غير متطابقة. يرجى إعادة الإدخال'
                return render(request,'accountdash/change_password.html',{'err':err}) 
            else:           
                user = authenticate(username=request.user,password=oldpassword)
                if user != None:
                    user = User.objects.get(username=request.user)
                    user.set_password(newpassword1)
                    user.save()
                    logout(request)
                    return redirect('mylogin')
                else:
                    err = 'كلمة المرور القديمة غير صحيحة.. يرجى إعادة الإدخال'
                    return render(request,'accountdash/change_password.html',{'err':err})            
    return render(request,'accountdash/change_password.html')
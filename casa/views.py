from django.shortcuts import redirect, render, get_object_or_404
from .forms import ReceiptForm
from .models import Receipt

from django.core.paginator import Paginator


def add_receipt(request):
    form = ReceiptForm()
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('receipt_list')
    return render(request, 'casa/add_r.html', {'form': form})


def receipt_list(request):
    receipts = Receipt.objects.all()
    # context = {
    #     'receipts': receipts
    # }
    paginator = Paginator(receipts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'casa/receipt_list1.html', {'page_obj': page_obj})


def edit_receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, pk=receipt_id)
    if request.method == 'GET':
        form = ReceiptForm(instance=receipt)
        return render(request, 'casa/edit_receipt.html', {'form': form})
    else:
        try:
            form = ReceiptForm(request.POST, instance=receipt)
            form.save()
            return redirect('receipt_list')
        except:
            return render(request, 'casa/msg.html')


def delete_receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, pk=receipt_id)
    # if request.method == 'POST':
    receipt.delete()
    return redirect('receipt_list')


def msg(request):
    return render(request, 'casa/msg.html')

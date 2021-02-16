from django import forms
from .models import Invoice


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'customer_id',
            'customer_name',
            'from_date',
            'balance_to',
            'proid',
            'tyear',
            'Invoice_no',
            'invoice_amount',
            'balance',
            'notes'

        ]
        labels = {
            'customer_id': 'رقم الجهة',
            'customer_name': 'إسم الجهة',
            'from_date' : 'تاريخ التسوية من :',
            'balance_to': 'حى تاريخ :',
            'proid' :'الفترة',
            'tyear': 'السنة',
            'Invoice_no': 'رقم الفاتورة',
            'invoice_amount': 'قيمة الفاتورة',
            'balance': 'قيمة التسوية',
            'notes':'ملاحظات',

        }
        # widgets = {
        #     'customer_id': forms.TextInput(attrs={'class': 'form-control text-right', 'id': 'inputEstimatedBudget'},),
        #     'customer_name': forms.TextInput(attrs={'class': 'form-control text-right'}),
        #     'from_date': forms.TextInput(attrs={'class': 'form-control text-right'}),
        #     'balance_to': forms.TextInput(attrs={'class': 'form-control text-right'}),
        #     'proid': forms.TextInput(attrs={'class': 'form-control text-right'}),
        #     'tyear': forms.TextInput(attrs={'class': 'form-control text-right'}),
        #     'Invoice_no': forms.TextInput(attrs={'class': 'form-control text-right'}),
        #     'invoice_amount': forms.NumberInput(attrs={'class': 'form-control text-right'}),
        #     'notes': forms.TextInput(attrs={'class': 'form-control text-right'}),
        #     'balance': forms.NumberInput(attrs={'class': 'form-control text-right'})

        # }

from django import forms
from django.forms import fields
from .models import Receipt


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = [
            'receipt_no',
            'receipt_date',
            'receipt_amount',
            'receipt_notes',
            'customer_name',
            'customer_id',

        ]
        labels = {
            'receipt_no': 'رقم الإيصال',
            'receipt_date': 'التاريخ',
            'receipt_amount': 'القيمة',
            'receipt_notes': 'ملاحظات',
        }
        widgets = {
            'receipt_no': forms.TextInput(attrs={'class': 'form-control text-right', 'id': 'inputEstimatedBudget'},),
            'receipt_date': forms.DateInput(attrs={'class': 'form-control text-right'}),
            'receipt_amount': forms.NumberInput(attrs={'class': 'form-control text-right', 'step': '0.1'}),
            'receipt_notes': forms.TextInput(attrs={'class': 'form-control text-right'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control text-right'}),
            'customer_id': forms.TextInput(attrs={'class': 'form-control text-right'}),

        }

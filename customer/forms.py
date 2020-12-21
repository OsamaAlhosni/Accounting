from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'id',
            'customer_name',
            'beginig_balance',
            'is_active',
        ]
        labels = {
            'id': 'رقم الجهة',
            'customer_name': 'إسم الجهة',
            'beginig_balance': 'ديون مرحلة',
            'is_active':'حالة الحساب',
        }


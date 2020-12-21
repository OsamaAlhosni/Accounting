from django import forms
from django.forms import fields
from .models import Receipt
from customer.models import Customer


class ReceiptForm(forms.ModelForm):
    receipt_no = forms.CharField(max_length=128, help_text="Please enter the name.")
    receipt_date = forms.CharField(max_length=128, help_text="Please enter the name of the autthor.")
    receipt_amount = forms.SlugField(help_text="Please enter the slug")
    customer_id = forms.ModelChoiceField(queryset=Customer.objects.values('customer_name'))
    receipt_notes = forms.CharField(max_length=128, help_text="Please enter the name of the autthor.")
    customer_name = forms.CharField(max_length=128, help_text="Please enter the name of the autthor.")
    
    def save(self, commit=True):
       instance = super().save(commit=False)
       pub = self.cleaned_data['customer_id']
       instance.customer_id = pub[0]
       instance.save(commit)
       return instance

    class Meta:
        model = Receipt
        fields = ('receipt_no', 'receipt_date','receipt_amount','customer_id')
    
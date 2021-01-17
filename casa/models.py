from django.db import models
from customer.models import Customer

class PaymentType(models.Model):
    payment_type = models.CharField(max_length=150)

    def __str__(self):
        return self.payment_type
class Bank(models.Model):
    name=models.CharField(max_length= 150)

    def __str__(self):
        return self.name
class ReceiptType(models.Model):
    type_desc = models.CharField(max_length=150)

    def __str__(self):
        return self.type_desc
class Receipt(models.Model):
    receipt_no = models.IntegerField()
    receipt_date = models.DateTimeField(blank=False, null=False)
    receipt_amount = models.DecimalField(
        max_digits=19, decimal_places=3, blank=False, null=False)
    receipt_notes = models.CharField(max_length=250, blank=True, null=True)
    receipt_created = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    priod = models.IntegerField(null=True,blank=True)
    syear = models.IntegerField(null=True,blank=True)
    invoice_no = models.CharField(max_length=100, blank=True, null=True)
    receipt_type = models.ForeignKey(ReceiptType,on_delete=models.CASCADE,null=True,blank=True)
    check_no = models.CharField(max_length=150,null=True,blank=True)
    bank = models.ForeignKey(Bank,on_delete=models.CASCADE,null=True,blank=True)
    transfare_no = models.CharField(max_length= 150,blank=True,null=True)
    payment_type = models.ForeignKey(PaymentType,on_delete=models.CASCADE,null=True,blank=True)
    transfare_date = models.DateField(null=True,blank=True)

   
from django.db import models
from customer.models import Customer

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
    

   
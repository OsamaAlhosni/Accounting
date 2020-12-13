from django.db import models


class Receipt(models.Model):
    receipt_no = models.IntegerField()
    receipt_date = models.DateTimeField(blank=False, null=False)
    receipt_amount = models.DecimalField(
        max_digits=19, decimal_places=3, blank=False, null=False)
    receipt_notes = models.CharField(max_length=250, blank=True, null=True)
    receipt_created = models.DateField(auto_now_add=True)
    customer_id = models.IntegerField()
    customer_name = models.CharField(max_length=200, blank=True,null=True)

    def __str__(self) :
        return self.customer_name,self.receipt_no,self.receipt_amount
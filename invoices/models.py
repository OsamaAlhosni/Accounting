from django.db import models


class Invoice(models.Model):
    customer_id = models.IntegerField()
    customer_name = models.CharField(max_length=200, null=True, blank=True)
    from_date = models.DateField(
        null=True, blank=True)
    balance_to = models.DateField(null=True, blank=True)
    proid = models.IntegerField(default=0)
    tyear = models.IntegerField(blank=True, null=True)
    Invoice_no = models.CharField(max_length=30, null=True, blank=True)
    invoice_amount = models.DecimalField(
        max_digits=19, decimal_places=3, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    balance = models.DecimalField(
        max_digits=19, decimal_places=3, blank=True, null=True)
    commited = models.BooleanField(default=False)
    imported_date = models.DateTimeField(
        auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.customer_name
        # , self.Invoice_no, self.proid, self.invoice_amount

class Customer(models.Model):
    customer_name = models.CharField(max_length=200, null=False, blank=False)
    beginig_balance = models.DecimalField(max_digits=19,decimal_places=3,null=True,blank=True)
    is_active = models.BooleanField(default=True)

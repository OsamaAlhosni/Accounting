from django.db import models
from django.contrib.auth.models import User


class Treasury(models.Model):
    treasury_name = models.CharField(max_length=200, blank=False, null=False)
    beginig_balance = models.DecimalField(
        max_digits=19, decimal_places=3, blank=True, null=True, default=0)
    is_active = models.BooleanField(blank=True, null=True, default=True)

    def __str__(self):
        return self.treasury_name


class Transaction(models.Model):
    trans_date = models.DateField(auto_now=True, blank=False, null=False)
    trans_amount = models.DecimalField(
        max_digits=19, decimal_places=3, blank=False, null=False)
    trans_desc = models.CharField(max_length=250, blank=True, null=True)
    treasury = models.ForeignKey(Treasury, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    created_by =models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
      return str(self.trans_amount)


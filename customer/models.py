from django.db import models

class Customer(models.Model):
    customer_name = models.CharField(max_length=200, null=False, blank=False)
    beginig_balance = models.DecimalField(max_digits=19,decimal_places=3,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
      return self.customer_name
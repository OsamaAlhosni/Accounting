from django.db import models

class CustomerCatogry(models.Model):
  type_desc=models.CharField(max_length=150)

  def __str__(self):
      return self.type_desc
      
class Customer(models.Model):
    customer_name = models.CharField(max_length=200, null=False, blank=False)
    beginig_balance = models.DecimalField(max_digits=19,decimal_places=3,null=True,blank=True,default=0)
    is_active = models.BooleanField(default=True)
    customer_cat= models.ForeignKey(CustomerCatogry,on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
      return self.customer_name

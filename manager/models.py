from django.db import models

class Manager(models.Model):
    manager_name = models.CharField(max_length=200,null=False,blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.manager_name
    

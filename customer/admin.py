from django.contrib import admin
from .models import Customer,CustomerCatogry


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'beginig_balance', 'customer_cat','is_active')


admin.site.register(Customer,CustomerAdmin)
admin.site.register(CustomerCatogry)
from django.contrib import admin


from .models import Receipt,ReceiptType,Bank,PaymentType


#
admin.site.register(Receipt)
admin.site.register(ReceiptType)
admin.site.register(Bank)
admin.site.register(PaymentType)

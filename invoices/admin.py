from django.contrib import admin


from .models import Invoice


class InvoiceAdmin(admin.ModelAdmin):
    list_display=('customer_id','proid','tyear','commited','imported_date')
    list_filter =('proid','tyear','commited','imported_date')
    search_fields = ('customer_name',  )    

admin.site.register(Invoice,InvoiceAdmin)
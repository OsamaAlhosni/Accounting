from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Invoice


#
admin.site.register(Invoice)


class InvoiceAdmin(ImportExportModelAdmin):
    list_display = ('customer_id', 'customer_name', 'balance', 'from_date',
                    'balance_to', 'proid', 'Invoice_no', 'invoice_amount', 'upload_date', 'notes')

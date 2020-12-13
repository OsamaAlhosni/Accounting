from import_export import resources
from .models import Invoice


class InvoiceResource(resources.ModelResource):
    class meta:
        model = Invoice

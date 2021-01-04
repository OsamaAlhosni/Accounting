
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('accountdash.urls')),
    path('invoices/', include('invoices.urls')),
    path('casa/', include('casa.urls')),
    path('customer/', include('customer.urls')),
    path('manager/', include('manager.urls')),
    path('admin/', admin.site.urls),

]

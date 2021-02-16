
from django.urls import path
from .import views
urlpatterns = [

    path('', views.invoice_list, name='invoice_list'),
    path('search/', views.search, name='search'),
    path('upload_invoice/', views.upload_invoice, name='upload_invoice'),
    path('<int:invoice_id>', views.edit_invoice, name='edit_invoice'),
    path('invoice-detail/<int:invoice_id>', views.invoice_detail, name='invoice_detail'),
    path('delete_invoice/<int:invoice_id>',
         views.delete_invoice, name='delete_invoice'),
    path('save_to_database/', views.save_to_database, name='save_to_database'),
    path('create_invoice/', views.create_invoice, name='create_invoice'),


]

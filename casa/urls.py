
from django.urls import path
from .import views
urlpatterns = [

    path('', views.add_receipt, name='add_receipt'),
    path('receipt_list', views.receipt_list, name='receipt_list'),
    path('msg', views.msg, name='msg'),
    path('receipt/<int:receipt_id>', views.edit_receipt, name='edit_receipt'),
    path('delete_receipt/<int:receipt_id>',
         views.delete_receipt, name='delete_receipt'),
    path('casa_search', views.casa_search, name='casa_search'),
    


]

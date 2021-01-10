

from django.urls import path
from . import views
urlpatterns = [

    path('', views.index, name='index'),
    path('ticketdash', views.index2, name='index2'),
    path('ticket_list', views.ticket_list, name='ticket_list'),
    path('sales_report', views.sales_report, name='sales_report'),
    path('receipt_report', views.receipt_report, name='receipt_report'),    
    path('total_inv_rec_report', views.total_inv_rec_report, name='total_inv_rec_report'),        
    path('mylogout', views.mylogout, name='mylogout'),
    path('mylogin', views.mylogin, name='mylogin'),
    path('change_password', views.change_password, name='change_password'),
]

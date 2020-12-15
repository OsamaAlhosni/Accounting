

from django.urls import path
from . import views
urlpatterns = [

    path('', views.index, name='index'),
    path('ticketdash', views.index2, name='index2'),
    path('ticket_list', views.ticket_list, name='ticket_list'),
]

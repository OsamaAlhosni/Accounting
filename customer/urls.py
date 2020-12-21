
from django.urls import path
from .import views
urlpatterns = [

    path('customer', views.customer_list, name='customer_list'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('edit_customer/<int:customer_id>', views.edit_customer, name='edit_customer'),
    path('delete_customer/<int:customer_id>',
         views.delete_customer, name='delete_customer'),
    


]

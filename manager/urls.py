
from django.urls import path
from . import views

urlpatterns = [
    path('',views.manager_list ,name='manager_list'),
    

]


from django.urls import path
from . import views

urlpatterns = [
    path('',views.manager_list ,name='manager_list'),
    path('add_user',views.add_user ,name='add_user'),
    path('users_list',views.users_list ,name='users_list'),  
    path('delete_user/<int:user_id>',views.delete_user, name='delete_user'),
    path('edit_user/<int:user_id>',views.edit_user, name='edit_user'),    

    

]

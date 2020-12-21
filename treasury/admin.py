from django.contrib import admin
from .models import Treasury,Transaction

admin.site.register(Transaction)
admin.site.register(Treasury)


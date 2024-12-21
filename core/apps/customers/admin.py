from django.contrib import admin

from core.apps.customers.models import Customer
from django.contrib.auth.models import Group, User
# Register your models here.


@admin.register(Customer)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name',
                    'last_name', 'in_process', 'role')


admin.site.unregister(User)
admin.site.unregister(Group)
